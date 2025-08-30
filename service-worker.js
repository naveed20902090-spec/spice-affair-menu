const CACHE_NAME = 'spice-affair-menu-v1';
const SHELL_CACHE = 'spice-affair-shell-v1';
const IMAGE_CACHE = 'spice-affair-images-v1';

// Files to cache for offline functionality
const SHELL_FILES = [
  '/',
  '/index.html',
  '/menu.json',
  '/manifest.json',
  '/assets/logo.png',
  '/assets/chalkboard-background.webp'
];

// Install event - cache shell files
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) => {
        console.log('Service Worker: Caching shell files');
        return cache.addAll(SHELL_FILES);
      })
      .then(() => {
        console.log('Service Worker: Shell files cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Service Worker: Error caching shell files:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== SHELL_CACHE && cacheName !== IMAGE_CACHE) {
              console.log('Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }
  
  // Handle different types of requests
  if (isImageRequest(request)) {
    // Network-first strategy for images
    event.respondWith(handleImageRequest(request));
  } else if (isShellRequest(request)) {
    // Cache-first strategy for shell files
    event.respondWith(handleShellRequest(request));
  } else {
    // Default network-first for other requests
    event.respondWith(handleDefaultRequest(request));
  }
});

// Check if request is for an image
function isImageRequest(request) {
  const url = new URL(request.url);
  return url.pathname.includes('/assets/') && 
         (url.pathname.endsWith('.webp') || 
          url.pathname.endsWith('.png') || 
          url.pathname.endsWith('.jpg') || 
          url.pathname.endsWith('.jpeg'));
}

// Check if request is for shell files
function isShellRequest(request) {
  const url = new URL(request.url);
  return SHELL_FILES.some(file => {
    if (file === '/') {
      return url.pathname === '/' || url.pathname === '/index.html';
    }
    return url.pathname === file;
  });
}

// Handle image requests with network-first strategy
async function handleImageRequest(request) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache the successful response
      const cache = await caches.open(IMAGE_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    throw new Error('Network response not ok');
  } catch (error) {
    // Fall back to cache
    console.log('Service Worker: Network failed for image, trying cache:', request.url);
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return placeholder image if nothing in cache
    return new Response(
      '<svg width="280" height="200" viewBox="0 0 280 200" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="280" height="200" fill="#f8f6f0"/><path d="M140 100L120 80L160 80L140 100Z" fill="#ccc"/></svg>',
      {
        headers: {
          'Content-Type': 'image/svg+xml',
          'Cache-Control': 'no-cache'
        }
      }
    );
  }
}

// Handle shell requests with cache-first strategy
async function handleShellRequest(request) {
  try {
    // Try cache first
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      // Update cache in background
      updateCacheInBackground(request);
      return cachedResponse;
    }
    
    // Fall back to network
    console.log('Service Worker: Cache miss for shell file, trying network:', request.url);
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache the response
      const cache = await caches.open(SHELL_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('Service Worker: Error handling shell request:', error);
    
    // Return offline page or basic response
    if (request.url.includes('index.html') || request.url.endsWith('/')) {
      return new Response(
        '<!DOCTYPE html><html><head><title>Spice Affair - Offline</title></head><body><h1>Spice Affair</h1><p>You are offline. Please check your connection.</p></body></html>',
        { headers: { 'Content-Type': 'text/html' } }
      );
    }
    
    return new Response('Offline', { status: 503 });
  }
}

// Handle default requests with network-first strategy
async function handleDefaultRequest(request) {
  try {
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    console.log('Service Worker: Network failed for default request, trying cache:', request.url);
    const cachedResponse = await caches.match(request);
    return cachedResponse || new Response('Offline', { status: 503 });
  }
}

// Update cache in background for shell files
async function updateCacheInBackground(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(SHELL_CACHE);
      cache.put(request, networkResponse);
    }
  } catch (error) {
    console.log('Service Worker: Background cache update failed:', error);
  }
}

// Handle messages from the main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Periodic background sync for cache updates (if supported)
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(updateShellCache());
  }
});

// Update shell cache
async function updateShellCache() {
  try {
    const cache = await caches.open(SHELL_CACHE);
    const promises = SHELL_FILES.map(async (file) => {
      try {
        const response = await fetch(file);
        if (response.ok) {
          return cache.put(file, response);
        }
      } catch (error) {
        console.log('Service Worker: Failed to update cache for:', file);
      }
    });
    
    await Promise.allSettled(promises);
    console.log('Service Worker: Shell cache updated');
  } catch (error) {
    console.error('Service Worker: Error updating shell cache:', error);
  }
}


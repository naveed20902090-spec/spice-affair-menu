# Spice Affair - Digital QR Menu

A super-fast, browse-only QR menu for Spice Affair food cart featuring a chalkboard design with horizontal card carousels. Built as a single static page with PWA capabilities and complete print materials.

## 🚀 Quick Start

1. **Download** the complete package
2. **Upload** files to your web hosting service
3. **Update** menu items and prices in `menu.json`
4. **Print** QR codes from the `print/` folder
5. **Deploy** to https://menu.spiceaffair.com

## 📁 Project Structure

```
spice-affair-menu/
├── index.html              # Main menu page (responsive, accessible)
├── menu.json               # Menu data (easily editable)
├── service-worker.js       # PWA offline functionality
├── manifest.json           # PWA installation support
├── generate_qr.py          # QR code generation script
├── assets/                 # Images and icons
│   ├── logo.png           # Spice Affair logo
│   ├── chalkboard-background.webp  # Background texture (<80KB)
│   ├── icon-*.png         # PWA icons (multiple sizes)
│   └── *.webp             # Menu item images (<100KB each)
├── print/                  # Print-ready materials
│   ├── qr-menu.svg        # QR code (vector format)
│   ├── qr-menu-1000.png   # QR code (1000x1000px)
│   ├── qr-poster-A4.pdf   # A4 poster for printing
│   └── qr-sticker-4x4in.pdf  # 4x4 inch sticker
├── README.md              # This documentation
└── test-results.md        # Testing and performance results
```

## 🌐 Deployment Instructions

### Option 1: Netlify (Recommended)

1. **Create Netlify Account**: Sign up at [netlify.com](https://netlify.com)

2. **Deploy via Drag & Drop**:
   ```bash
   # Create deployment package
   zip -r spice-affair-menu.zip . -x "*.git*" "*.DS_Store*" "generate_qr.py"
   ```
   - Go to Netlify dashboard
   - Drag and drop the zip file
   - Your site will be live at `https://random-name.netlify.app`

3. **Custom Domain Setup**:
   - In Netlify dashboard, go to Site Settings > Domain Management
   - Add custom domain: `menu.spiceaffair.com`
   - Follow DNS configuration instructions
   - SSL certificate will be automatically provisioned

4. **Update QR Codes** (if domain changes):
   ```bash
   # Edit generate_qr.py to update MENU_URL
   python3 generate_qr.py
   # Re-upload the updated print files
   ```

### Option 2: GitHub Pages

1. **Create GitHub Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Spice Affair QR Menu"
   git branch -M main
   git remote add origin https://github.com/yourusername/spice-affair-menu.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Your site will be live at `https://yourusername.github.io/spice-affair-menu`

3. **Custom Domain** (optional):
   - Add `CNAME` file with your domain: `menu.spiceaffair.com`
   - Configure DNS A records to point to GitHub Pages IPs

### Option 3: Traditional Web Hosting

1. **Upload Files**:
   - Use FTP/SFTP to upload all files to your web server
   - Ensure the domain points to `https://menu.spiceaffair.com`

2. **Server Configuration** (optional):
   ```apache
   # .htaccess for Apache
   <IfModule mod_headers.c>
       Header set Cache-Control "max-age=31536000" "expr=%{REQUEST_URI} =~ m#\.(webp|png|jpg|svg)$#"
       Header set Cache-Control "max-age=86400" "expr=%{REQUEST_URI} =~ m#\.(html|json|js|css)$#"
   </IfModule>
   ```

## ✏️ Editing the Menu

### Adding/Removing Menu Items

Edit `menu.json` to update your menu:

```json
{
  "sections": [
    {
      "id": "masala",
      "name": "Masala",
      "items": [
        {
          "name": "Egg Masala Dosa",
          "description": "Crispy dosa with spiced egg masala filling",
          "price": "$12.99",
          "image": "assets/egg-masala-dosa.webp"
        }
      ]
    }
  ]
}
```

### Updating Prices

Simply change the `"price"` field in `menu.json`:
```json
"price": "$12.99"  // Change from "TBD" to actual price
```

### Adding New Sections

1. Add new section to `menu.json`
2. Update navigation tabs in `index.html` (search for `nav-tabs`)
3. Add corresponding images to `assets/` folder

### Replacing Images

1. **Optimize new images**:
   - Format: WebP (preferred) or PNG/JPG
   - Size: Maximum 100KB each
   - Dimensions: 280x200px (landscape) recommended

2. **Replace files**:
   - Upload new image to `assets/` folder
   - Update filename in `menu.json`
   - Keep same aspect ratio for consistency

## 🖨️ Print Materials

### QR Code Files

- **qr-menu.svg**: Vector format for high-quality printing
- **qr-menu-1000.png**: High-resolution raster (1000x1000px)
- **Error Correction**: Level H (30% damage tolerance)

### Print-Ready Materials

- **qr-poster-A4.pdf**: Full-size poster for walls/windows
- **qr-sticker-4x4in.pdf**: Small stickers for tables/counters

### Regenerating QR Codes

If you change the domain URL:

1. **Edit the script**:
   ```python
   # In generate_qr.py, update:
   MENU_URL = "https://your-new-domain.com"
   ```

2. **Run the generator**:
   ```bash
   python3 generate_qr.py
   ```

3. **Print new materials** from the updated PDF files

## 🔧 Technical Specifications

### Performance
- **Initial Load**: <200KB total payload
- **Images**: <100KB each, WebP format with lazy loading
- **Lighthouse Score**: 95+ on mobile
- **No External Dependencies**: Self-contained, no CDNs required

### Browser Support
- **Modern Browsers**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **Mobile**: iOS Safari 12+, Chrome Mobile 60+
- **PWA Features**: Service Worker, Web App Manifest

### Accessibility
- **WCAG 2.1 AA Compliant**: Proper contrast, keyboard navigation
- **Screen Reader Support**: Semantic HTML, ARIA labels
- **Touch Targets**: Minimum 44px for mobile usability

## 🛠️ Customization

### Changing Colors

Edit CSS variables in `index.html`:
```css
:root {
    --primary-green: #2d5a3d;    /* Main brand color */
    --light-green: #4a7c59;      /* Hover states */
    --cream: #f8f6f0;            /* Card backgrounds */
}
```

### Modifying Layout

- **Card Size**: Change `.menu-card { flex: 0 0 280px; }`
- **Sections**: Add/remove tabs in navigation
- **Fonts**: Currently uses system fonts for performance

### Adding Analytics

Add before closing `</head>` tag:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 📱 PWA Features

### Installation
- Users can install the menu as an app on their phones
- Works offline with cached content
- Fast loading with service worker

### Updating Content
- Menu updates automatically when users refresh
- Images cached for offline viewing
- Service worker handles network failures gracefully

## 🐛 Troubleshooting

### Common Issues

1. **Images not loading**:
   - Check file paths in `menu.json`
   - Ensure images are in `assets/` folder
   - Verify file extensions match (case-sensitive)

2. **QR code doesn't work**:
   - Verify the URL in `generate_qr.py`
   - Ensure domain is accessible
   - Check QR code error correction level

3. **Mobile layout issues**:
   - Test on actual devices, not just browser dev tools
   - Check viewport meta tag is present
   - Verify touch targets are large enough

4. **Service worker not working**:
   - Must be served over HTTPS (except localhost)
   - Check browser console for errors
   - Clear browser cache and reload

### Performance Optimization

1. **Further compress images**:
   ```bash
   # Using imagemagick
   convert input.jpg -quality 85 -resize 280x200^ output.webp
   ```

2. **Minify HTML/CSS/JS**:
   - Use online minifiers before deployment
   - Remove comments and whitespace

3. **Enable compression**:
   - Configure gzip/brotli on your server
   - Most hosting providers enable this by default

## 📞 Support

For technical issues or customization requests:
- Check `test-results.md` for performance metrics
- Review browser console for error messages
- Ensure all files are uploaded correctly

## 📄 License

This project is created for Spice Affair food cart. All images and branding materials are property of Spice Affair.

---

**Ready to serve delicious dosas with a digital twist! 🌶️**


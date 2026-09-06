#!/usr/bin/env python3
"""
GdbMTB Static Site Generator for GitHub Pages & Static Hosting
==============================================================

This script exports all dynamic Flask routes into pre-rendered static HTML
files and bundles all static assets (CSS, JS, SVGs, images, PDF) into a
standalone directory (default: 'docs/') ready for GitHub Pages.

Usage:
------
# 1. Export for GitHub Pages (default: base path '/MTBdatabase', output 'docs')
python export_static.py

# 2. Export for custom domain or root domain (e.g. www.gdbmtb.cn or username.github.io)
python export_static.py --base-path ""

# 3. Export and immediately launch a local preview server
python export_static.py --serve
"""

import os
import sys
import shutil
import re
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Import the existing Flask app
import GdbMTB

ROUTES = [
    ('/', 'index.html'),
    ('/home', 'home'),
    ('/browser/QualityandFeature', 'browser/QualityandFeature'),
    ('/browser/classification', 'browser/classification'),
    ('/browser/reference', 'browser/reference'),
    ('/browser/EnvironmentalMetadata', 'browser/EnvironmentalMetadata'),
    ('/browser/MagnetosomeGeneClusters', 'browser/MagnetosomeGeneClusters'),
    ('/tree-taxa', 'tree-taxa'),
    ('/tree-tree', 'tree-tree'),
    ('/statistics', 'statistics'),
    ('/downloads', 'downloads'),
    ('/about', 'about'),
]

INTERNAL_NAV_ROUTES = [
    'browser/QualityandFeature',
    'browser/classification',
    'browser/reference',
    'browser/EnvironmentalMetadata',
    'browser/MagnetosomeGeneClusters',
    'tree-taxa',
    'tree-tree',
    'statistics',
    'downloads',
    'about',
    'home',
]


def adjust_links(html_content: str, base_path: str) -> str:
    """
    Adjust absolute paths in HTML to support GitHub Pages project subpaths
    (e.g., /MTBdatabase/) or custom root domains.
    """
    prefix = '/' + base_path.strip('/') if base_path.strip('/') else ''

    # 1. Adjust static asset URLs (CSS, JS, images, iframes, favicon)
    # Match href="/static/... or src="/static/... or url('/static/...
    if prefix:
        html_content = re.sub(r'href=["\']/static/+', f'href="{prefix}/static/', html_content)
        html_content = re.sub(r'src=["\']/static/+', f'src="{prefix}/static/', html_content)
        html_content = re.sub(r'url\(["\']?/static/+', f'url("{prefix}/static/', html_content)
    else:
        html_content = re.sub(r'href=["\']/static/+', 'href="/static/', html_content)
        html_content = re.sub(r'src=["\']/static/+', 'src="/static/', html_content)
        html_content = re.sub(r'url\(["\']?/static/+', 'url("/static/', html_content)
    
    # 2. Adjust internal navigation links in navbar and page content
    for route in INTERNAL_NAV_ROUTES:
        # Match href="/route" or href="/route/"
        html_content = re.sub(
            rf'href=["\']/{route}(/)?(["\'])',
            rf'href="{prefix}/{route}/\2',
            html_content
        )

    # 3. Adjust home / navbar-brand link: href="/"
    html_content = re.sub(r'href=["\']/["\']', f'href="{prefix}/"', html_content)

    # 4. Adjust JavaScript dynamic links (in tree-taxa.html and statistics.html)
    html_content = html_content.replace(
        '"/browser/classification?search="',
        f'"{prefix}/browser/classification/?search="'
    )

    return html_content


def generate_404_html(base_path: str) -> str:
    """Generate a clean 404 page for GitHub Pages."""
    prefix = '/' + base_path.strip('/') if base_path.strip('/') else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Page Not Found - GdbMTB</title>
  <meta http-equiv="refresh" content="3;url={prefix}/">
  <link rel="stylesheet" href="{prefix}/static/dist/css/bootstrap.min.css">
</head>
<body class="bg-light d-flex align-items-center" style="min-height: 100vh;">
  <div class="container text-center py-5">
    <h1 class="display-1 text-muted">404</h1>
    <h2>Page Not Found</h2>
    <p class="lead">The requested page could not be located. Redirecting to <a href="{prefix}/">GdbMTB Home</a> in 3 seconds...</p>
    <a href="{prefix}/" class="btn btn-primary mt-3">Back to Home</a>
  </div>
</body>
</html>
"""


def export_site(base_path: str = '/MTBdatabase', output_dir: str = 'docs'):
    """Renders all Flask routes to static HTML and copies static assets."""
    print("=" * 60)
    print("  GdbMTB Static Site Exporter")
    print("=" * 60)
    print(f"[*] Base Path  : '{base_path}'")
    print(f"[*] Output Dir : '{output_dir}'")
    print("-" * 60)

    # Prepare output directory
    if os.path.exists(output_dir):
        print(f"[-] Cleaning existing output directory '{output_dir}'...")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Use Flask's built-in test client
    client = GdbMTB.app.test_client()

    print("[+] Rendering routes to HTML:")
    rendered_count = 0

    for route, target_path in ROUTES:
        res = client.get(route)
        if res.status_code != 200:
            print(f"    [!] ERROR: Failed to render {route} (Status {res.status_code})")
            continue

        raw_html = res.data.decode('utf-8')
        processed_html = adjust_links(raw_html, base_path)

        if target_path.endswith('.html'):
            file_path = os.path.join(output_dir, target_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)
            print(f"    ✓ {route:<35} -> {target_path}")
            rendered_count += 1
        else:
            # 1. Write target_path/index.html (standard directory structure)
            dir_index_path = os.path.join(output_dir, target_path, 'index.html')
            os.makedirs(os.path.dirname(dir_index_path), exist_ok=True)
            with open(dir_index_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)

            # 2. Also write target_path.html (fallback for direct URL requests)
            flat_html_path = os.path.join(output_dir, f"{target_path}.html")
            os.makedirs(os.path.dirname(flat_html_path), exist_ok=True)
            with open(flat_html_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)

            print(f"    ✓ {route:<35} -> {target_path}/index.html & {target_path}.html")
            rendered_count += 1

    # Copy static assets
    print("-" * 60)
    print("[+] Copying static directory...")
    static_src = os.path.join(os.path.dirname(__file__), 'static')
    static_dst = os.path.join(output_dir, 'static')
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)
        print(f"    ✓ Copied '{static_src}' to '{static_dst}'")
    else:
        print(f"    [!] Warning: static directory not found at {static_src}")

    # Create .nojekyll (CRITICAL for GitHub Pages to prevent Jekyll bypassing files)
    nojekyll_path = os.path.join(output_dir, '.nojekyll')
    with open(nojekyll_path, 'w', encoding='utf-8') as f:
        f.write('')
    print("    ✓ Created '.nojekyll' file for GitHub Pages")

    # Create 404.html
    not_found_path = os.path.join(output_dir, '404.html')
    with open(not_found_path, 'w', encoding='utf-8') as f:
        f.write(generate_404_html(base_path))
    print("    ✓ Created '404.html' error page")

    print("-" * 60)
    print(f"[✓] Export completed successfully! Total pages: {rendered_count}")
    print(f"    All static files are saved in: {os.path.abspath(output_dir)}")
    print("=" * 60)


def serve_preview(output_dir: str = 'docs', port: int = 8000):
    """Launches a simple HTTP server to preview the static export locally."""
    abs_dir = os.path.abspath(output_dir)
    os.chdir(abs_dir)
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"\n[🚀] Local preview server running at: http://localhost:{port}/")
    print(f"    Serving directory: {abs_dir}")
    print("    Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server stopped.")


def main():
    parser = argparse.ArgumentParser(description="Export GdbMTB Flask app to static HTML for GitHub Pages.")
    parser.add_argument(
        '--base-path',
        type=str,
        default='/MTBdatabase',
        help="Base path URL for GitHub Pages (e.g. '/MTBdatabase', or '' for custom/root domain)."
    )
    parser.add_argument(
        '--output',
        type=str,
        default='docs',
        help="Output directory path (default: 'docs' for GitHub Pages direct deployment)."
    )
    parser.add_argument(
        '--serve',
        action='store_true',
        help="Start a local HTTP preview server after export."
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help="Port for the preview server (default: 8000)."
    )

    args = parser.parse_args()
    export_site(base_path=args.base_path, output_dir=args.output)

    if args.serve:
        serve_preview(output_dir=args.output, port=args.port)


if __name__ == '__main__':
    main()

import { readFileSync, writeFileSync, renameSync, rmSync } from 'fs';
import { join } from 'path';

// Move popup.html from dist/src/ to dist/ and fix paths
const distPath = './dist';
const srcPopupPath = join(distPath, 'src', 'popup.html');
const destPopupPath = join(distPath, 'popup.html');

try {
  // Read the HTML file
  let html = readFileSync(srcPopupPath, 'utf8');

  // Fix absolute paths to relative paths
  html = html.replace('src="/popup.js"', 'src="./popup.js"');
  html = html.replace('href="/assets/', 'href="./assets/');

  // Write to root of dist
  writeFileSync(destPopupPath, html);

  // Remove src directory
  rmSync(join(distPath, 'src'), { recursive: true, force: true });

  console.log('✓ Fixed popup.html paths and moved to dist root');
} catch (error) {
  console.error('Error fixing build:', error.message);
  process.exit(1);
}

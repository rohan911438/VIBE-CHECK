@echo off
echo Starting Git deployment...

echo.
echo Stage 1: Adding all files...
git add .

echo.
echo Stage 2: Committing changes...
git commit -m "Fix GitHub Pages deployment - update workflow and add missing files"

echo.
echo Stage 3: Pushing to main branch...
git push origin main

echo.
echo Deployment initiated! Check GitHub Actions tab for progress.
echo Your site will be available at: https://rohan911438.github.io/VIBE-CHECK/
echo.
pause

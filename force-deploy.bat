@echo off
echo Forcing GitHub Pages deployment...

echo.
echo Step 1: Making a small change to force rebuild...
echo. >> README.md
echo Last deployment: %date% %time% >> README.md

echo.
echo Step 2: Committing changes...
git add .
git commit -m "Force deployment - %date%"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo Step 4: Your website links:
echo Main site: https://rohan911438.github.io/VIBE-CHECK/
echo Quiz page: https://rohan911438.github.io/VIBE-CHECK/quiz.html
echo.
echo Check the Actions tab on GitHub to monitor deployment progress.
echo.
pause

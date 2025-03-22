@echo off
echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Making initial commit...
git commit -m "Initial commit: Paperscraper project setup"

echo Git repository initialized successfully!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub (https://github.com/new)
echo 2. Copy the repository URL
echo 3. Run the following command (replace URL with your repository URL):
echo    git remote add origin URL
echo    git push -u origin main
pause 
# WOS Windhowler Tracker

Ever wondered exactly how much damage you need to clear the Windhowler trial in Whiteout Survival? Same. 

This project is a combination of a static web calculator and a local AI data pipeline. We figured out that the game dynamically scales the boss's HP window. So, instead of guessing, we use OCR to scrape exact damage numbers from player battle report screenshots, run the data through a Huber regression model to filter out the game's UI rounding nonsense, and spit out the exact start and window sizes for every level.

## How it works
1. You drop screenshots into the local Admin Dashboard.
2. EasyOCR (running on your GPU) rips the damage, percent, and level.
3. The ML script calculates the exact HP window.
4. It exports a JSON block directly into `exact_levels.js`.
5. The static HTML site (`wos-formula-refiner.html`) uses that JS file to give perfect predictions to anyone visiting the site.

## Running it locally
Make sure you have Python installed, along with a decent GPU for the OCR.

```bash
pip install easyocr pandas scikit-learn streamlit
```

To spin up the admin dashboard to process new screenshots:
```bash
streamlit run admin_dashboard.py
```
(Note: You can drag and drop multiple images at once, or click the upload box and paste directly from your clipboard!)

## Hosting
The main calculator (`wos-formula-refiner.html`) is built to run entirely as a static site. It's designed to be hosted directly on GitHub Pages. No backend needed—all the heavy AI lifting is done locally on your machine before you push the updated formulas!

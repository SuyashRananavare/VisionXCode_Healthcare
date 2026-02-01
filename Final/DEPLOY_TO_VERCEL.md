# Deploy to Vercel

Vercel is a great option for hosting this Flask application serverless-ly.

## Prerequisites
1.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2.  **GitHub Account**: Push your code to a GitHub repository.

## Steps

1.  **Push to GitHub**:
    *   Create a new repository on GitHub.
    *   Push all files in this directory to that repository.
    *   *Ensure `vercel.json` and `requirements.txt` are included.*

2.  **Import to Vercel**:
    *   Go to your [Vercel Dashboard](https://vercel.com/dashboard).
    *   Click **"Add New..."** -> **"Project"**.
    *   Select the GitHub repository you just created.

3.  **Configure Project**:
    *   **Framework Preset**: Select "Other" (Vercel usually auto-detects Python/Flask via the `vercel.json` file).
    *   **Root Directory**: Leave as `./`.
    *   **Environment Variables**: Add any if needed (none required for this base app).
    *   **Build & Output Settings**: Leave default. The `vercel.json` file handles the configuration.

4.  **Deploy**:
    *   Click **"Deploy"**.
    *   Vercel will build your Python environment and launch the app.

## Troubleshooting
*   **Static Files**: The `vercel.json` is configured to serve `/static` files directly. If images don't load, ensure they are in the `static` folder.
*   **Logs**: If you see a "500 Server Error", check the "Logs" tab in the Vercel dashboard. It usually means a missing dependency in `requirements.txt` or a syntax error.

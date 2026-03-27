/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // Next 16 defaults to Turbopack in production builds (e.g., Vercel).
  // Adding an explicit empty config avoids webpack/turbopack mismatch errors.
  turbopack: {},
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        ...(config.watchOptions || {}),
        // Ignore backend/python churn to keep Next dev CPU lower.
        ignored: ["**/backend/**", "**/__pycache__/**", "**/.venv/**"],
      }
    }
    return config
  },
}

export default nextConfig

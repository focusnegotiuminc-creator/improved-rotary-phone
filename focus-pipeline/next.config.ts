import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow streaming responses from API routes
  experimental: {
    serverActions: {
      bodySizeLimit: "2mb",
    },
  },
};

export default nextConfig;

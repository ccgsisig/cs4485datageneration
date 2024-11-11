// src/pages/HomePage.js

import React from "react";
import Navbar from "../components/header";
import ParticlesBackground from "../components/threeBackground";
import { useAuth0 } from "@auth0/auth0-react";

const HomePage = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="relative h-screen" id="home">
      <Navbar />
      {/* Ensure the particles background is behind other elements */}
      <ParticlesBackground className="absolute top-0 left-0 w-full h-full z-0" />
      <div className="flex h-full items-center justify-center px-6 lg:px-8 relative z-10">
        <div className="text-center mx-auto">
          <h1 className="text-foreground dark:text-light-gray font-bold text-4xl md:text-3xl xl:text-6xl">
            MomentoData
          </h1>
          <p className="mt-8 text-gray-500 dark:text-gray-600 max-w-xl mx-auto">
            Empowering next-generation 5G insights with resilient, adaptive, and
            high-speed analytics solutions tailored for the modern era.
          </p>
          <div className="mt-8 flex justify-center gap-y-4 gap-x-6">
            <button
              onClick={() => loginWithRedirect()}
              className="relative flex h-11 items-center justify-center px-6 before:absolute before:inset-0 before:rounded-full before:bg-electricblue dark:before:bg-vibrant-green before:transition before:duration-300 hover:before:scale-105 active:before:scale-95"
            >
              <span className="relative text-base font-semibold text-background">
                Login or Sign Up
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

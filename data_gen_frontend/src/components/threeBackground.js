import React, { useEffect } from "react";
import "particles.js";

const ParticlesBackground = () => {
  useEffect(() => {
    if (typeof window !== "undefined" && window.particlesJS) {
      window.particlesJS("particles-js", {
        particles: {
          number: {
            value: 200,
            density: {
              enable: true,
              value_area: 800,
            },
          },
          color: {
            value: ["#10B981", "#00FFFF", "#1E90FF", "#20B2AA", "#00BFFF"], // Cool colors: neon green, cyan, light blue, teal, sky blue
          },
          shape: {
            type: "circle",
            stroke: {
              width: 0,
              color: "#000000",
            },
            polygon: {
              nb_sides: 6,
            },
            image: {
              src: "img/github.svg",
              width: 100,
              height: 100,
            },
          },
          opacity: {
            value: 0.7,
            random: true,
          },
          size: {
            value: 8,
            random: true,
          },
          line_linked: {
            enable: false,
          },
          move: {
            enable: true,
            speed: 3,
            direction: "none",
            random: true,
            straight: false,
            out_mode: "out",
            bounce: false,
          },
        },
        interactivity: {
          detect_on: "window",
          events: {
            onhover: {
              enable: true,
              mode: "bubble",
            },
            onclick: {
              enable: true,
              mode: "push",
            },
            resize: true,
          },
          modes: {
            grab: {
              distance: 400,
              line_linked: {
                opacity: 1,
              },
            },
            bubble: {
              distance: 200,
              size: 10,
              duration: 1,
              opacity: 0.8,
              speed: 2,
            },
            repulse: {
              distance: 60,
              duration: 0.4,
            },
            push: {
              particles_nb: 6,
            },
            remove: {
              particles_nb: 2,
            },
          },
        },
        retina_detect: true,
      });
    }
  }, []);

  return (
    <div
      id="particles-js"
      className="absolute top-0 left-0 w-full h-full z-0 transform transition-all"
    />
  );
};

export default ParticlesBackground;

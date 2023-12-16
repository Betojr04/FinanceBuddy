import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { HeroSection } from "../component/HeroSection";
import { FeatureSection } from "../component/FeatureSection.js";
import { InteractiveSection } from "../component/InteractiveSection.js";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <main>
      <HeroSection />
      <FeatureSection />
      <InteractiveSection />
    </main>
  );
};

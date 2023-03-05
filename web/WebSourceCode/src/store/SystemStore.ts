import { BasicStore } from "./BasicStore";
import { storeToRefs } from "pinia";

export const SystemStore = () => {
  return {
    basicStore: BasicStore(),
  };
};

export const ref2 = storeToRefs;

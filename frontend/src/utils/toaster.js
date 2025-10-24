import { toast, Bounce } from "react-toastify";

const defaultToastConfig = {
  position: "bottom-center",
  autoClose: 5000,
  hideProgressBar: true,
  closeOnClick: true,
  pauseOnHover: false,
  draggable: false,
  progress: undefined,
  transition: Bounce,
};

export const toaster = {
  warnAuth: () => {
    toast.warn(
      "Vous devez vous authentifier pour accéder à cette page.",
      defaultToastConfig
    );
  },
  successDisconnected: () => {
    toast.success("Vous avez correctement été déconnecté.", defaultToastConfig);
  },
};

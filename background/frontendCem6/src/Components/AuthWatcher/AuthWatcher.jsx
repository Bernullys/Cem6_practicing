import { useEffect } from "react";
import { useLocation } from "react-router-dom";

// Add here all routes that require login
const protectedRoutes = ["/allApp"];

export default function AuthWatcher() {
    const location = useLocation();

    useEffect(() => {
        const currentPath = location.pathname;
        const token = localStorage.getItem("access_token");

        const isProtected = protectedRoutes.includes(currentPath);

        if (!isProtected && token) {
            localStorage.removeItem("access_token");
            console.log("Token removed because route is not protected");
        }
    }, [location]);

    return null;
}

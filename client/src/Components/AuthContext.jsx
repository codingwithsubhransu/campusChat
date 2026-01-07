import { createContext, useContext, useEffect, useState } from "react";
import isAuthenticated from "./api/isAuthenticated";

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadUser = async () => {
            const auth = await isAuthenticated();
            if (auth.authenticated) {
                setUser(auth.user);
            }
            setLoading(false);
        }
        loadUser();
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
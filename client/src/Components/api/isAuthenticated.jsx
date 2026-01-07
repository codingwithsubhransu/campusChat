import authAxios from "./apiConfig";

export default async function isAuthenticated() {
    try {
        const response = await authAxios.get('/current-user');
        return { authenticated: true, user: response.data.username  };
    } catch (error) {
        return { authenticated: false , user: null  };
    }
};
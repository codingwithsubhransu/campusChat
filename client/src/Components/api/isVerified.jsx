import authAxios from "./apiConfig";

export const isAuthenticated = async () => {
    try {
        const response = await authAxios.get('/current_user_is_verified');
        return response.data.isVerified;
    } catch (error) {
        console.error('Error checking authentication status:', error);
        return false;
    }
};
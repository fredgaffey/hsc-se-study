// auth.js
import { requestBackend } from './api';

/**
 * Wrapper func - server request to register user - setting token in browser.  
 * @param {String} email 
 * @param {String} password 
 * @param {String} name 
 * @returns {Promise<Object>}  
 */
export const adminAuthRegister = async (email, password, name) => {
    const body = { email, password, name };
    // Clear any old tokens before registering
    sessionStorage.removeItem("session_token");
    sessionStorage.removeItem("csrf_token");
    
    const response = await requestBackend("POST", "admin/auth/register", null, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    // Session token is now stored in HTTP-only cookie (set by backend)
    // Only CSRF token needs to be stored in sessionStorage
    sessionStorage.setItem("csrf_token", response.csrf_token);
    sessionStorage.setItem("owner", email);
    return response;
};

/**
 * Wrapper func - server request to login user - also token set in browser.
 * @param {String} email 
 * @param {String} password 
 * @returns {Promise<Object>}  
 */

export const adminAuthLogin = async (email, password) => {
    const body = { email, password };
    // Clear any old tokens before login
    sessionStorage.removeItem("session_token");
    sessionStorage.removeItem("csrf_token");
    
    const response = await requestBackend("POST", "admin/auth/login", null, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    // Session token is now stored in HTTP-only cookie (set by backend)
    // Only CSRF token needs to be stored in sessionStorage
    sessionStorage.setItem("csrf_token", response.csrf_token);
    sessionStorage.setItem("owner", email);
    return response;
}

/**
 * Wrapper func - server request to logout user - removing token and owner from browser storage.
 */
export const adminAuthLogout = async () => {
    // const sessionToken = localStorage.getItem("session_token");
    // const csrfToken = localStorage.getItem("csrf_token");
    // Session token is sent automatically via cookie
    const tokens = {
        csrf_token: sessionStorage.getItem("csrf_token")
    }
    const ownerEmailAddress = sessionStorage.getItem("owner");

    if (!tokens || !ownerEmailAddress) {
        throw new Error("Cannot logout - no tokens or owner email found");
    }

    const response = await requestBackend("POST", "admin/auth/logout", tokens, null, null);
    if (response.error) {
        throw new Error(response.error);
    }

    sessionStorage.removeItem("csrf_token");
    sessionStorage.removeItem("owner");
    // Session token cookie will be cleared by backend on logout
}

/**
 * Wrapper func - server request to check if token is valid.
 * @returns {Boolean} - true if token is valid, false otherwise
 */
export const validateUserToken = async () => {
    // Session token is sent automatically via cookie
    const tokens = {
        csrf_token: sessionStorage.getItem("csrf_token")
    }
    
    // TODO: Implement proper token validation
    // using admin/games endpoint to check if token is valid as there is no endpoint to check token validity
    const response = await requestBackend("GET", "admin/games", tokens, null, null);
    if (response.error) {
        return false
    }
    return true;
}
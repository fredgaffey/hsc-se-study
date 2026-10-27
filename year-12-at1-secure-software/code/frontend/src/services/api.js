export const BACKEND_PORT = 8000
export const BACKEND_URL = `http://localhost:${BACKEND_PORT}`
/**
 * API wrapper for the backend func to make requests
 * @param {String} method - GET, POST, PUT, DELETE
 * @param {String} route - the route to the backend
 * @param {Object} tokens - token object - session and csrf tokens as keys for backend auth
 * @param {Obj} payload - the payload to be sent to the backend
 * @param {String} query - the query string to be sent to the backend
 * @returns {Promise<Object>} - the response from the backend
 */
export const requestBackend = async (method, route, tokens, payload, query) => {
    let url = `${BACKEND_URL}/${route}`
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',  // This allows cookies to be sent with requests
    };

    if (query) {
        url += `?${query}`;
    }

    if (tokens && tokens.csrf_token) {
        // Session token is sent automatically via cookie (with credentials: 'include')
        // Only CSRF token needs to be sent in header
        options.headers["X-CSRF-Token"] = tokens.csrf_token;
    }

    if (payload) {
        options.body = JSON.stringify(payload);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        return response.json()
    } catch (error) {
        console.error("Error", error)
        throw new Error(error.message); 
    }
}
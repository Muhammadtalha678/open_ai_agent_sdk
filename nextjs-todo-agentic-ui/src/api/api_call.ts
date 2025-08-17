import axios, { AxiosError, isAxiosError } from "axios"

export const apiCallGet = async (url: string) => {
    try {
        const response = await axios.get(url)
        const data = response.data
        return data
    } catch (error) {
        console.error("API Error:", error);
        // throw new Error(error?.response?.data?.detail || "Failed to fetch data");
    }
}
export const apiCallPost = async (url: string, input: string) => {
    try {
        const response = await axios.post(url, { query: input })
        const data = response.data
        return data
    } catch (error) {
        if (isAxiosError(error)) {
            // The error is an AxiosError, so you can safely access Axios-specific properties
            const axiosError: AxiosError = error;
            console.error('Axios Error:', axiosError.message);
            if (axiosError.response) {
                // Access response details for HTTP errors
                console.error('Status:', axiosError.response.status);
                console.error('Data:', axiosError.response.data);
            }
        } else {
            // Handle other types of errors (e.g., network errors, unexpected exceptions)
            console.error('Unknown Error:', error);
        }

    }
}
import apiClient from "../../../api/apiClient";

type RegisterPayload = {
    email: string;
    username: string;
    password: string
}

type LoginPayload = {
    email: string;
    password: string;
}

export const register = async (payload: RegisterPayload) => {
    return await apiClient.post("/auth/register", payload);
}

export const login = async (payload: LoginPayload) => {
    return await apiClient.post("/auth/login", payload);
}
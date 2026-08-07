import apiClient from "../../../api/apiClient";

export const getSessions = async (params: {page: number, limit: number}) => {
    return apiClient.get("/analyze/sessions", { params })
}

export const getSessionById = async (id: string) => {
    return apiClient.get(`/analyze/${id}`)
}

export const uploadCSV = async (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    return apiClient.post("/analyze/upload", formData)
}
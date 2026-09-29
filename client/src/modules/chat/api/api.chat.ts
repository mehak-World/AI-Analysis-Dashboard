import apiClient from "../../../api/apiClient";

export const sendMsg = (sessionId: string, question: string) => {
    return apiClient.post(`/chat/${sessionId}`, { question })
}
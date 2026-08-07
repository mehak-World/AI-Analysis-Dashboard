import {useState, useEffect} from 'react'
import { getSessions } from '../api/api.dashboard';
import type { AllSessionsRes } from '../types/dashboard.types';

const useSessions = () => {
    const [sessions, setSessions] = useState<AllSessionsRes[]>([])
    const [loading, setLoading] = useState(false);
    const [pagination, setPagination] = useState({
        page: 1, 
        limit: 10,
        total: 0
    })
    const [error, setError] = useState("")

    const fetchSessions = async () => {
        try{
            setLoading(true)
            const res = await getSessions({ page: pagination.page, limit: pagination.limit})
            setSessions(res?.data?.data)
            setPagination(res?.data?.pagination)
        }
        catch(err){
            console.log(err)
        }
        finally{
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchSessions()
    }, [pagination.page, pagination.limit])

    return {
        sessions,
        setSessions,
        loading,
        setLoading,
        fetchSessions,
        pagination,
        setPagination,
        error,
        setError
    }
}

export default useSessions

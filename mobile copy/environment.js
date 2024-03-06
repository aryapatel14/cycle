// import Constants from "expo-constants";
import { ENV_API_URL } from '@env';

const getEnvVars = () => {
    return { API_URL: ENV_API_URL };
}

export default getEnvVars;
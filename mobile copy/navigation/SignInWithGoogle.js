import React, { useState, useEffect } from "react";
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
// import * as AuthSession from 'expo-auth-session';
import FormButton from "../components/FormButton";

WebBrowser.maybeCompleteAuthSession();

// Loading env variables
import {
    GOOGLE_CLOUD_WEB_ID,
    GOOGLE_CLOUD_ANDROID_ID,
    GOOGLE_CLOUD_IOS_ID,
} from '@env';

const SignInWithGoogle = ({ successFn }) => {
    const [accessToken, setAccessToken] = useState(null);
    // const [user, setUser] = useState(null);
    const [request, response, promptAsync] = Google.useAuthRequest({
        clientId: GOOGLE_CLOUD_WEB_ID,
        iosClientId: GOOGLE_CLOUD_IOS_ID,
        androidClientId: GOOGLE_CLOUD_ANDROID_ID,
        // redirectUri: AuthSession.makeRedirectUri({})
    });

    useEffect(() => {
        if (response?.type === "success") {
            setAccessToken(response.authentication.accessToken);
            // accessToken && fetchUserInfo();
            successFn(response);
        }
    }, [response, accessToken]);


    return (
        <FormButton
            iconName="google"
            btnTitle="Sign in with Google"
            isHighlight={true}
            disabled={!request}
            onPress={() => promptAsync()}
        />
    );
};

export default SignInWithGoogle;
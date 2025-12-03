"use client";
import { Amplify } from "aws-amplify";
import type { ResourcesConfig } from "aws-amplify";

const amplifyConfig: ResourcesConfig = {
  Auth: {
    Cognito: {
      userPoolId: String(process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID),
      userPoolClientId: String(process.env.NEXT_PUBLIC_COGNITO_USER_POOL_CLIENT_ID),
    },
  },
};

Amplify.configure(amplifyConfig, { ssr: true });

export default function AmplifyCognitoConfig() {
  return null;
}
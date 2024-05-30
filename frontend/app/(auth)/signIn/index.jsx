import React from "react"

import { View, Text, ScrollView, StyleSheet } from 'react-native'
import { Image } from 'expo-image';
import { SafeAreaView } from 'react-native-safe-area-context'

import AuthForm from '../../components/authForm'

import {styles} from "./sign-inStyles"

import AquawareLogo from "../../../assets/AquwareLogoSVG.svg"

const SignIn = () => {
  const [formValues, setFormValues] = React.useState({ email: '', password: '' });

  const handleFormChange = (newValues) => {
    setFormValues(newValues);
    console.log(newValues)
  };

  const handleLogin = () => {

    // Here goes the logic by Mario

    console.log('Logging in with:', formValues);
  };
  return (
   <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Image
          source={AquawareLogo}
          style={styles.image}
          contentFit="cover"
        />
        <AuthForm 
        title="Login" //Possible to make its fields and functionality on submit depending on the title, whether is Login or Register 
        onFormChange={handleFormChange}
        // keyboardType="email-address"
        onLogin = {handleLogin}
        />
      </View>
   </SafeAreaView>
  );
}

export default SignIn

import { View, Text, StyleSheet} from 'react-native'
import React from 'react'
import CustomButton from './components/customButton'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Image } from 'expo-image';
import { Redirect, router } from 'expo-router';

import globalStyles  from './globalStyles';

import AquawareLogo from '../assets/AquawareLogo.svg'
import WaterIcon from '../assets/authSvg/IconWater.svg'

const AuthLayout = () => {
  return (
    <SafeAreaView style = {styles.container}>
      <Image
        source={AquawareLogo}
        style={styles.image}
        contentFit="cover"
      />
      <Text style={styles.logo}>Aquaware</Text>
      <Text style={styles.welcomeMessage}>Добре дошли в Aquaware, вашият незаменим партнъор в следенето и пестенето на вода!  {/* на потреблението на вода, където може да се научите и да пестите вода с нашите безценни съвети! */}</Text>
      {/* <Text>Sign-up</Text> */}
      {/* <Link href="/sign-up">Влез</Link> */}
      <CustomButton title={'Влезте в профила си'} handlePress={() =>  router.push('signIn')
      }/>
      {/* <CustomButton title={'Създай профил'} handlePress={() => console.log('click') }/> */}
    </SafeAreaView>
  )
}

export default AuthLayout

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 50,
    // background:'linear-gradient(#e66465, #9198e5)',
    paddingTop: 40
  },
  logo: {
    fontSize: 25,
    fontWeight: 'bold',
    color: globalStyles.primaryColor,
  },
  welcomeMessage: {
    fontSize: 18,
    textAlign: 'center'
  },
  image: {
    width: 160,
    height: 150,
  }

  
})
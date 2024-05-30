import { View, Text } from 'react-native'
import React from 'react'
import { Stack } from 'expo-router'
import {StatusBar} from 'expo-status-bar'

const AuthLayout = () => {
  return (
    <>
      <Stack>
        <Stack.Screen
          name='signIn/index'
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name='sign-up'
          options={{
            headerShown: false,
          }}
        />
      </Stack>

      {/* <StatusBar backgroundColor='gray' style='light'/> */}
    </>
  )
}

export default AuthLayout
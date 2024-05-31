import {styles} from "./authFormStyles"

import { View, Text, TextInput, TouchableOpacity } from 'react-native'
import React from 'react'

import  globalStyles  from '../globalStyles';
import CustomButton from './customButton';


import GooglePath from '../../assets/authSvg/google.png'
import FacebookPath from '../../assets/authSvg/facebook.png'

const FormField = ({title, value, placeholder, onFormChange, formValues, setFormValues, type, ...props}) => {
  const handleChange = (name, value) => {
    const updatedValues = { ...formValues, [name]: value };
    setFormValues(updatedValues);
    onFormChange(updatedValues);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.inputName}>{title}</Text>
      <View style={styles.inputContainer}>
        <TextInput style={styles.inputField} value={formValues[type]} onChangeText={(text) => handleChange(type, text)}
        secureTextEntry={title === "Парола" ? true : false}></TextInput>
      </View>
    </View>
  )
}

const AuthForm = ({title, value, placeholder, onFormChange, onLogin, ...props}) => {
  let errorMsg = '';
  const [formValues, setFormValues] = React.useState({
    email: '',
    password: '',
  })
  const handleChangeText = (e) => {
    console.log(e.value)
  }

  return (
    <>
      <FormField title={"Е-Поща"} type={'email'} onFormChange={onFormChange} formValues={formValues} setFormValues={setFormValues} />
      <FormField title={"Парола"} type={'password'} onFormChange={onFormChange} formValues={formValues} setFormValues={setFormValues} />
      <Text style={styles.errorMsg}>{errorMsg}</Text>
      <CustomButton title={'Влез'} additionalStyles={{marginTop: 15,}} handlePress={onLogin}/>
      <Text style={{fontSize: 14, fontWeight: 'bold', textTransform: 'uppercase'}}>или</Text>
      <View style={styles.thirdPartyAuthBox}>
        <CustomButton 
        title={'Влез с Google'} 
        additionalStyles={{ 
          width: '35%',
          padding: 5,
          // borderRadius: 30, 
          backgroundColor: '#FFF',
          borderColor: globalStyles.primaryColor,
          borderWidth: 1, 
        }}
        imagePath={GooglePath}
          />
        <CustomButton 
        title={'Влез с Facebook'} 
        additionalStyles={{
          width: '35%',
          padding: 5,
          // borderRadius: 30, 
          backgroundColor: '#FFF',
          borderColor: globalStyles.primaryColor,
          borderWidth: 1, 
        }}
        imagePath={FacebookPath}
            />
      </View>
      <View>
      <TouchableOpacity >
        <Text style={styles.link}>
          Забравихте си паролата? <Text onPress={() => console.log('click')} style={styles.linkBold}>Смени парола.</Text>
        </Text>
      </TouchableOpacity>
      </View>
      <View>
      <TouchableOpacity >
        <Text style={styles.link}>
          Нямате профил? <Text onPress={() => console.log('click')} style={styles.linkBold}>Създай профил.</Text>
        </Text>
      </TouchableOpacity>
      </View>
    </>
  )
}

export default AuthForm


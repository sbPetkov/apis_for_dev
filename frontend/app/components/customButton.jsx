import { TouchableOpacity, Text, StyleSheet, Image } from 'react-native'
import React from 'react';

import { styles } from "./customButtonStyles"

const CustomButton = ({title, handlePress, isLoading, additionalStyles, imagePath}) => {
  return (
    <TouchableOpacity
    onPress={handlePress}
    activeOpacity={0.7}
    style={[styles.container, isLoading ? {opacity : 50} : null, additionalStyles]}
    disabled={isLoading}
    >
      
      { imagePath ? <Image source={imagePath} /> :<Text style={styles.btn}>{title}</Text>}
    </TouchableOpacity>
  )
}

export default CustomButton;


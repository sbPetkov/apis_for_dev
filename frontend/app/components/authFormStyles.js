import { StyleSheet } from "react-native"
import globalStyles from "../globalStyles"

export const styles = StyleSheet.create({
    container: {
        // flex: 1,
        width: '100%',
        height: 'auto',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 5,
        // marginBottom: 15,
    },
    errorMsg: {
      color: 'red',
    },
    thirdPartyAuthBox: {
      flexDirection: 'row',
      width: '80%',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 15,
    },
    inputName: {
      fontSize: 18,
      fontWeight: '500'
    },
    inputContainer: {
        width: '80%',
        height: 40,
        borderWidth: 2,
        borderColor: globalStyles.primaryColor,
        justifyContent: 'center',
        borderRadius: 13,
        paddingLeft: 10,
        paddingRight: 10,
        backgroundColor: '#fff'
    },
    inputField: {
      fontSize: 18,
      textDecorationStyle: 'none'
    },
      link: {
        color: 'blue',
        textDecorationLine: 'none',
      },
      linkBold: {
        fontWeight: 'bold',
        textDecorationLine: 'underline',
      }
})
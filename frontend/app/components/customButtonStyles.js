import {StyleSheet} from 'react-native'
import globalStyles from '../globalStyles'

export const styles = StyleSheet.create({
    container: {
        width: '60%',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: globalStyles.primaryColor,
        padding: 16,
        borderRadius: 16,
    },
    btn: {
        textAlign: 'center',
        fontSize: 16,
        fontWeight: 'bold',
        color: '#fff'
    }
})
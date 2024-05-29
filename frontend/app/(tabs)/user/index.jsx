import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, Button, Alert } from 'react-native';

const User = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const server = "http://192.168.1.3:8000";

    const handleRegister = async () => {
        console.log(name, email, password, repeatPassword);
        if (!name || !email || !password || !repeatPassword) {
            Alert.alert('Грешка', 'Моля, попълнете всички полета');
            return;
        }

        if (password !== repeatPassword) {
            Alert.alert('Грешка', 'Паролите не съвпадат');
            return;
        }
        try {
            const response = await fetch(`${server}/profile/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: email,
                    password: password,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log(`DATA is ${data.username}`);
            Alert.alert('Успех', `Регистрирани сте като ${data.username}`);
        } catch (error) {
            console.error('Error:', error);
            Alert.alert('Грешка', 'Проблем при връзката със сървъра');
        }

    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Регистрация</Text>
            <TextInput
                style={styles.input}
                placeholder="Име"
                value={name}
                onChangeText={setName}
            />
            <TextInput
                style={styles.input}
                placeholder="Имейл"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
            />
            <TextInput
                style={styles.input}
                placeholder="Парола"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            <TextInput
                style={styles.input}
                placeholder="Потвърди парола"
                value={repeatPassword}
                onChangeText={setRepeatPassword}
                secureTextEntry
            />
            <Button title="Регистрация" onPress={handleRegister} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 16,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        marginBottom: 16,
        textAlign: 'center',
    },
    input: {
        height: 40,
        borderColor: '#ccc',
        borderWidth: 1,
        marginBottom: 12,
        paddingLeft: 8,
    },
});

export default User;

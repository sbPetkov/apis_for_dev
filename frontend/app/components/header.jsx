import { View, Pressable, Image } from "react-native";

import AntDesignI from "react-native-vector-icons/AntDesign";

import { styles } from "./headerStyles.js";

import PROFILE_PIC from "../../assets/blank-profile.png";
import LOGO_COVER from "../../assets/logo-cover.jpeg";

export const Header = ({ showProfilePic }) => {
  const onArrowPress = () => {
    console.log("TODO: redirect to home screen");
  };
  const onProfilePress = () => {
    console.log("TODO: redirect to profile screen");
  };
  return (
    <View style={styles.container}>
      <Pressable onPress={showProfilePic ? onProfilePress : onArrowPress}>
        {showProfilePic ? (
          <View>
            <Image style={styles.pics} source={PROFILE_PIC} />
          </View>
        ) : (
          <AntDesignI name={"arrowleft"} size={35} style={styles.icon} />
        )}
      </Pressable>
      <Image style={styles.pics} source={LOGO_COVER} />
    </View>
  );
};

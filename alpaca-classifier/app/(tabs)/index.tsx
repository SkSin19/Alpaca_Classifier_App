import { Image } from 'expo-image';
import { StyleSheet, View, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Upload, RefreshCcw } from 'lucide-react-native';
import React from 'react';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

export default function HomeScreen() {
  const [isUploading, setIsUploading] = React.useState(false);
  const [selectedImage, setSelectedImage] = React.useState<string | null>(null);

  const checkPermission = async (): Promise<boolean> => {
    const { status } = await ImagePicker.getMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      const { status: newStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (newStatus !== 'granted') {
        alert('Permission to access media library is required!');
        return false;
      }
    }
    return true;
  };

  const handleImageUpload = async () => {
    setIsUploading(true);

    const hasPermission = await checkPermission();
    if (!hasPermission) {
      setIsUploading(false);
      return;
    }

    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 1,
      });

      if (!result.canceled) {
        setSelectedImage(result.assets[0].uri);
      }
    } catch {
      alert('Failed to pick image. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleClearImage = () => {
    setSelectedImage(null);
  };

  const ClassifyImage = async () => {
    if (!selectedImage) {
      alert('Please select an image first!');
      return;
    }

    setIsUploading(true);
    try {
      const response = await axios.post('http://localhost:5000/classify', {
        image: selectedImage
      });
      alert('Image classified successfully!');
    } catch {
      alert('Failed to classify image. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };


  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Alpaca Classifier</Text>
        <Text style={styles.subtitle}>Upload an image to classify</Text>
      </View>

      {selectedImage ? (
        <View style={styles.imageContainer}>
          <Image source={{ uri: selectedImage }} style={styles.image} />
          <TouchableOpacity style={styles.clearButton} onPress={handleClearImage}>
            <RefreshCcw size={18} color="#fff" />
          </TouchableOpacity>
        </View>
      ) : (
        <TouchableOpacity style={styles.uploadArea} onPress={handleImageUpload}>
          <Upload size={48} color="#fff" style={styles.icon} />
          <Text style={styles.uploadText}>Tap to upload image</Text>
          <Text style={styles.uploadHint}>Supported formats: JPG, PNG</Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity
        style={[styles.button, isUploading && styles.buttonLoading]}
        onPress={ClassifyImage}
        disabled={isUploading}
      >
        {isUploading ? (
          <ActivityIndicator size="small" color="#fff" style={styles.spinner} />
        ) : (
          <Text style={styles.buttonText}>Classify Image</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
  },
  imageContainer: {
    width: '100%',
    height: 200,
    backgroundColor: '#111',
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  clearButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(0,0,0,0.55)',
    borderRadius: 20,
    padding: 8,
  },
  uploadArea: {
    width: '100%',
    height: 200,
    backgroundColor: '#111',
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  icon: {
    marginBottom: 16,
  },
  uploadText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  uploadHint: {
    fontSize: 14,
    color: '#777',
  },
  button: {
    backgroundColor: '#4f46e5',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonLoading: {
    opacity: 0.7,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  spinner: {
    marginRight: 8,
  },
});
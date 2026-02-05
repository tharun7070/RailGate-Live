import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    Alert,
    Linking,
    Platform,
} from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { CrossingStatus } from '../api/railApi';

interface Props {
    route: any;
    navigation: any;
}

const MapScreen: React.FC<Props> = ({ route, navigation }) => {
    const crossings: CrossingStatus[] = route.params?.crossings || [];
    const [selectedCrossing, setSelectedCrossing] = useState<CrossingStatus | null>(null);

    const initialRegion = {
        latitude: 12.9897,
        longitude: 77.7166,
        latitudeDelta: 0.1,
        longitudeDelta: 0.1,
    };

    const getMarkerColor = (status: string) => {
        switch (status) {
            case 'open': return '#10B981';
            case 'closing_soon': return '#F59E0B';
            case 'closed': return '#EF4444';
            default: return '#6B7280';
        }
    };

    const openGoogleMaps = (crossing: CrossingStatus, avoid: boolean = false) => {
        const destination = `${crossing.latitude},${crossing.longitude}`;
        const label = encodeURIComponent(crossing.name);

        let url = '';
        if (Platform.OS === 'ios') {
            url = `maps://app?daddr=${destination}&dirflg=d`;
            if (avoid) {
                url += '&avoid=highways'; // Approximate avoidance
            }
        } else {
            url = `https://www.google.com/maps/dir/?api=1&destination=${destination}&destination_place_id=${label}&travelmode=driving`;
            if (avoid) {
                url += '&avoid=highways';
            }
        }

        Linking.openURL(url).catch(() => {
            Alert.alert('Error', 'Could not open maps application');
        });
    };

    const submitFeedback = (crossing: CrossingStatus, status: 'open' | 'closed') => {
        Alert.alert(
            'Feedback Submitted',
            `Thank you for reporting this gate as ${status}!`,
            [{ text: 'OK' }]
        );
        // TODO: Call railApi.submitFeedback()
    };

    return (
        <View style={styles.container}>
            <MapView
                style={styles.map}
                provider={PROVIDER_GOOGLE}
                initialRegion={initialRegion}
            >
                {crossings.map((crossing) => (
                    <Marker
                        key={crossing.id}
                        coordinate={{
                            latitude: crossing.latitude,
                            longitude: crossing.longitude,
                        }}
                        title={crossing.name}
                        description={crossing.prediction.status}
                        pinColor={getMarkerColor(crossing.prediction.status)}
                        onPress={() => setSelectedCrossing(crossing)}
                    />
                ))}
            </MapView>

            {selectedCrossing && (
                <View style={styles.bottomSheet}>
                    <TouchableOpacity
                        style={styles.closeButton}
                        onPress={() => setSelectedCrossing(null)}
                    >
                        <Text style={styles.closeButtonText}>×</Text>
                    </TouchableOpacity>

                    <Text style={styles.sheetTitle}>{selectedCrossing.name}</Text>
                    <Text style={styles.sheetLocation}>{selectedCrossing.location}</Text>

                    <View style={styles.statusRow}>
                        <Text style={styles.statusLabel}>Status:</Text>
                        <Text
                            style={[
                                styles.statusValue,
                                { color: getMarkerColor(selectedCrossing.prediction.status) }
                            ]}
                        >
                            {selectedCrossing.prediction.status.replace('_', ' ').toUpperCase()}
                        </Text>
                    </View>

                    {selectedCrossing.prediction.next_closure && (
                        <Text style={styles.infoText}>
                            Next closure: {selectedCrossing.prediction.next_closure}
                        </Text>
                    )}

                    <View style={styles.buttonRow}>
                        <TouchableOpacity
                            style={[styles.button, styles.navigateButton]}
                            onPress={() => openGoogleMaps(selectedCrossing, false)}
                        >
                            <Text style={styles.buttonText}>🧭 Navigate</Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            style={[styles.button, styles.avoidButton]}
                            onPress={() => openGoogleMaps(selectedCrossing, true)}
                        >
                            <Text style={styles.buttonText}>🔀 Detour</Text>
                        </TouchableOpacity>
                    </View>

                    <View style={styles.feedbackRow}>
                        <TouchableOpacity
                            style={[styles.feedbackButton, styles.openButton]}
                            onPress={() => submitFeedback(selectedCrossing, 'open')}
                        >
                            <Text style={styles.feedbackButtonText}>✅ Gate Open</Text>
                        </TouchableOpacity>

                        <TouchableOpacity
                            style={[styles.feedbackButton, styles.closedButton]}
                            onPress={() => submitFeedback(selectedCrossing, 'closed')}
                        >
                            <Text style={styles.feedbackButtonText}>🚫 Gate Closed</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    map: {
        flex: 1,
    },
    bottomSheet: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: '#FFFFFF',
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
    },
    closeButton: {
        position: 'absolute',
        top: 12,
        right: 16,
        width: 32,
        height: 32,
        borderRadius: 16,
        backgroundColor: '#F3F4F6',
        justifyContent: 'center',
        alignItems: 'center',
    },
    closeButtonText: {
        fontSize: 28,
        color: '#6B7280',
        fontWeight: '300',
    },
    sheetTitle: {
        fontSize: 20,
        fontWeight: '700',
        color: '#111827',
        marginBottom: 4,
    },
    sheetLocation: {
        fontSize: 14,
        color: '#6B7280',
        marginBottom: 12,
    },
    statusRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 8,
    },
    statusLabel: {
        fontSize: 15,
        color: '#6B7280',
        marginRight: 8,
    },
    statusValue: {
        fontSize: 16,
        fontWeight: '700',
    },
    infoText: {
        fontSize: 14,
        color: '#6B7280',
        marginBottom: 16,
    },
    buttonRow: {
        flexDirection: 'row',
        gap: 12,
        marginBottom: 12,
    },
    button: {
        flex: 1,
        padding: 14,
        borderRadius: 10,
        alignItems: 'center',
    },
    navigateButton: {
        backgroundColor: '#3B82F6',
    },
    avoidButton: {
        backgroundColor: '#8B5CF6',
    },
    buttonText: {
        color: '#FFFFFF',
        fontSize: 15,
        fontWeight: '600',
    },
    feedbackRow: {
        flexDirection: 'row',
        gap: 12,
    },
    feedbackButton: {
        flex: 1,
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    openButton: {
        backgroundColor: '#ECFDF5',
    },
    closedButton: {
        backgroundColor: '#FEF2F2',
    },
    feedbackButtonText: {
        fontSize: 14,
        fontWeight: '600',
        color: '#111827',
    },
});

export default MapScreen;

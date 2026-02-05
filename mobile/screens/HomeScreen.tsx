import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    FlatList,
    RefreshControl,
    ActivityIndicator,
    TouchableOpacity,
    Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import railApi, { CrossingStatus } from '../api/railApi';
import CrossingCard from '../components/CrossingCard';

interface Props {
    navigation: any;
}

const HomeScreen: React.FC<Props> = ({ navigation }) => {
    const [crossings, setCrossings] = useState<CrossingStatus[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        loadCrossings();
    }, []);

    const loadCrossings = async () => {
        try {
            const allCrossings = await railApi.getCrossings();

            // Fetch detailed status for each crossing
            const detailedPromises = allCrossings.map(c =>
                railApi.getCrossingStatus(c.id)
            );

            const detailed = await Promise.all(detailedPromises);
            setCrossings(detailed);
        } catch (error) {
            console.error('Error loading crossings:', error);
            Alert.alert(
                'Connection Error',
                'Could not connect to server. Make sure the backend is running on http://localhost:8000'
            );
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const onRefresh = () => {
        setRefreshing(true);
        loadCrossings();
    };

    const getStatusCounts = () => {
        const open = crossings.filter(c => c.prediction.status === 'open').length;
        const closingSoon = crossings.filter(c => c.prediction.status === 'closing_soon').length;
        const closed = crossings.filter(c => c.prediction.status === 'closed').length;
        return { open, closingSoon, closed };
    };

    const counts = getStatusCounts();

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#3B82F6" />
                <Text style={styles.loadingText}>Loading crossings...</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <StatusBar style="dark" />

            <View style={styles.header}>
                <Text style={styles.headerTitle}>🚧 RailGate Live</Text>
                <Text style={styles.headerSubtitle}>Smart Railway Crossing Status</Text>
            </View>

            <View style={styles.summaryCard}>
                <Text style={styles.summaryTitle}>Current Status</Text>
                <View style={styles.summaryStats}>
                    <View style={styles.statItem}>
                        <Text style={styles.statNumber}>{counts.open}</Text>
                        <Text style={[styles.statLabel, { color: '#10B981' }]}>🟢 Open</Text>
                    </View>
                    <View style={styles.statDivider} />
                    <View style={styles.statItem}>
                        <Text style={styles.statNumber}>{counts.closingSoon}</Text>
                        <Text style={[styles.statLabel, { color: '#F59E0B' }]}>🟡 Closing Soon</Text>
                    </View>
                    <View style={styles.statDivider} />
                    <View style={styles.statItem}>
                        <Text style={styles.statNumber}>{counts.closed}</Text>
                        <Text style={[styles.statLabel, { color: '#EF4444' }]}>🔴 Closed</Text>
                    </View>
                </View>
            </View>

            <TouchableOpacity
                style={styles.mapButton}
                onPress={() => navigation.navigate('Map', { crossings })}
            >
                <Text style={styles.mapButtonText}>🗺️ View on Map</Text>
            </TouchableOpacity>

            <FlatList
                data={crossings}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <CrossingCard
                        crossing={item}
                        onPress={() => navigation.navigate('Details', { crossing: item })}
                    />
                )}
                refreshControl={
                    <RefreshControl
                        refreshing={refreshing}
                        onRefresh={onRefresh}
                        colors={['#3B82F6']}
                    />
                }
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <Text style={styles.emptyText}>No crossings available</Text>
                    </View>
                }
                contentContainerStyle={styles.listContent}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F3F4F6',
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F3F4F6',
    },
    loadingText: {
        marginTop: 12,
        fontSize: 16,
        color: '#6B7280',
    },
    header: {
        backgroundColor: '#3B82F6',
        paddingTop: 60,
        paddingBottom: 24,
        paddingHorizontal: 20,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: '800',
        color: '#FFFFFF',
        marginBottom: 4,
    },
    headerSubtitle: {
        fontSize: 15,
        color: '#DBEAFE',
    },
    summaryCard: {
        backgroundColor: '#FFFFFF',
        marginHorizontal: 16,
        marginTop: -20,
        marginBottom: 12,
        borderRadius: 12,
        padding: 16,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    summaryTitle: {
        fontSize: 16,
        fontWeight: '600',
        color: '#111827',
        marginBottom: 16,
    },
    summaryStats: {
        flexDirection: 'row',
        justifyContent: 'space-around',
    },
    statItem: {
        alignItems: 'center',
    },
    statNumber: {
        fontSize: 32,
        fontWeight: '800',
        color: '#111827',
        marginBottom: 4,
    },
    statLabel: {
        fontSize: 13,
        fontWeight: '600',
    },
    statDivider: {
        width: 1,
        backgroundColor: '#E5E7EB',
    },
    mapButton: {
        backgroundColor: '#3B82F6',
        marginHorizontal: 16,
        marginBottom: 12,
        padding: 14,
        borderRadius: 10,
        alignItems: 'center',
    },
    mapButtonText: {
        color: '#FFFFFF',
        fontSize: 16,
        fontWeight: '700',
    },
    listContent: {
        paddingBottom: 20,
    },
    emptyContainer: {
        padding: 40,
        alignItems: 'center',
    },
    emptyText: {
        fontSize: 16,
        color: '#6B7280',
    },
});

export default HomeScreen;

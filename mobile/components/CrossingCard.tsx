import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { CrossingStatus } from '../api/railApi';

interface Props {
    crossing: CrossingStatus;
    onPress: () => void;
}

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
    const getStatusColor = () => {
        switch (status) {
            case 'open': return '#10B981';
            case 'closing_soon': return '#F59E0B';
            case 'closed': return '#EF4444';
            default: return '#6B7280';
        }
    };

    const getStatusIcon = () => {
        switch (status) {
            case 'open': return '🟢';
            case 'closing_soon': return '🟡';
            case 'closed': return '🔴';
            default: return '⚪';
        }
    };

    const getStatusText = () => {
        switch (status) {
            case 'open': return 'Open';
            case 'closing_soon': return 'Closing Soon';
            case 'closed': return 'Closed';
            default: return 'Unknown';
        }
    };

    return (
        <View style={[styles.badge, { backgroundColor: getStatusColor() }]}>
            <Text style={styles.badgeIcon}>{getStatusIcon()}</Text>
            <Text style={styles.badgeText}>{getStatusText()}</Text>
        </View>
    );
};

const CrossingCard: React.FC<Props> = ({ crossing, onPress }) => {
    const prediction = crossing.prediction;

    const getReliabilityLabel = () => {
        const score = crossing.reliability_score;
        if (score >= 90) return '✅ Reliable';
        if (score >= 75) return '📊 Predictable';
        return '🔀 Sneaky';
    };

    return (
        <TouchableOpacity style={styles.card} onPress={onPress}>
            <View style={styles.header}>
                <View style={styles.titleContainer}>
                    <Text style={styles.title}>{crossing.name}</Text>
                    <Text style={styles.location}>{crossing.location}</Text>
                </View>
                <StatusBadge status={prediction.status} />
            </View>

            <View style={styles.details}>
                <View style={styles.detailRow}>
                    <Text style={styles.label}>Station:</Text>
                    <Text style={styles.value}>{crossing.nearest_station_name}</Text>
                </View>

                {prediction.next_closure && (
                    <View style={styles.detailRow}>
                        <Text style={styles.label}>Next Closure:</Text>
                        <Text style={[styles.value, styles.highlight]}>{prediction.next_closure}</Text>
                    </View>
                )}

                {prediction.estimated_duration_mins && (
                    <View style={styles.detailRow}>
                        <Text style={styles.label}>Duration:</Text>
                        <Text style={styles.value}>~{prediction.estimated_duration_mins} mins</Text>
                    </View>
                )}

                <View style={styles.detailRow}>
                    <Text style={styles.label}>Confidence:</Text>
                    <Text style={styles.value}>{prediction.confidence}%</Text>
                </View>

                <View style={styles.detailRow}>
                    <Text style={styles.label}>Reliability:</Text>
                    <Text style={styles.value}>{getReliabilityLabel()}</Text>
                </View>

                {prediction.trains_approaching > 0 && (
                    <View style={styles.detailRow}>
                        <Text style={styles.label}>Trains Approaching:</Text>
                        <Text style={styles.value}>{prediction.trains_approaching}</Text>
                    </View>
                )}

                {prediction.crowd_confirmations > 0 && (
                    <View style={styles.crowdInfo}>
                        <Text style={styles.crowdText}>
                            👥 {prediction.crowd_confirmations} people just passed this gate ✅
                        </Text>
                    </View>
                )}

                {prediction.detour_recommendation && (
                    <View style={styles.detourBox}>
                        <Text style={styles.detourTitle}>💡 Recommendation</Text>
                        <Text style={styles.detourMessage}>
                            {prediction.detour_recommendation.message}
                        </Text>
                    </View>
                )}
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    card: {
        backgroundColor: '#FFFFFF',
        borderRadius: 12,
        padding: 16,
        marginHorizontal: 16,
        marginVertical: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: 12,
    },
    titleContainer: {
        flex: 1,
        marginRight: 12,
    },
    title: {
        fontSize: 18,
        fontWeight: '700',
        color: '#111827',
        marginBottom: 4,
    },
    location: {
        fontSize: 14,
        color: '#6B7280',
    },
    badge: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 20,
    },
    badgeIcon: {
        fontSize: 12,
        marginRight: 4,
    },
    badgeText: {
        color: '#FFFFFF',
        fontWeight: '600',
        fontSize: 13,
    },
    details: {
        borderTopWidth: 1,
        borderTopColor: '#E5E7EB',
        paddingTop: 12,
    },
    detailRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 8,
    },
    label: {
        fontSize: 14,
        color: '#6B7280',
    },
    value: {
        fontSize: 14,
        fontWeight: '600',
        color: '#111827',
    },
    highlight: {
        color: '#F59E0B',
        fontWeight: '700',
    },
    crowdInfo: {
        backgroundColor: '#ECFDF5',
        borderLeftWidth: 3,
        borderLeftColor: '#10B981',
        padding: 10,
        borderRadius: 8,
        marginTop: 8,
    },
    crowdText: {
        fontSize: 13,
        color: '#065F46',
    },
    detourBox: {
        backgroundColor: '#EFF6FF',
        borderLeftWidth: 3,
        borderLeftColor: '#3B82F6',
        padding: 10,
        borderRadius: 8,
        marginTop: 8,
    },
    detourTitle: {
        fontSize: 13,
        fontWeight: '700',
        color: '#1E40AF',
        marginBottom: 4,
    },
    detourMessage: {
        fontSize: 13,
        color: '#1E40AF',
    },
});

export default CrossingCard;

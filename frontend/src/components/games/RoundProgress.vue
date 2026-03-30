<template>
    <div class="rounded-2xl border border-white/10 bg-white/5 px-6 py-4">
        <div class="flex items-center justify-between gap-4">
            <div>
                <span class="text-sm text-white/60">Round</span>
                <span class="ml-1 text-lg font-bold text-white">{{ currentRound }}</span>
                <span class="text-sm text-white/40"> / {{ totalRounds }}</span>
            </div>
            <div
                class="rounded-full border border-[#8c0a42]/40 bg-[#8c0a42]/20 px-3 py-1 text-xs font-semibold text-[#e0608a]"
            >
                {{ miniGameLabel }}
            </div>
        </div>

        <div class="mt-3 flex gap-1">
            <div
                v-for="i in totalRounds"
                :key="i"
                class="h-1.5 flex-1 rounded-full transition-all"
                :class="segmentClass(i)"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
    currentRound: number;
    totalRounds: number;
    gameType: 1 | 2 | 3;
}>();

const miniGameLabel = computed(() => {
    if (props.gameType === 1) return "Mini-Game 1";
    if (props.gameType === 2) return "Mini-Game 3";
    if (props.gameType === 3) return "Mini-Game 2";
    return "Mini-Game";
});

function segmentClass(index: number): string {
    if (index < props.currentRound) return "bg-[#8c0a42]";
    if (index === props.currentRound) return "bg-[#8c0a42]/50";
    return "bg-white/10";
}
</script>
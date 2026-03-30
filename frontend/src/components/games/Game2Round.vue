<template>
    <div class="space-y-4">
        <!-- Loading round data -->
        <div v-if="game2.loading.value" class="flex items-center justify-center py-16">
            <div class="text-sm text-white/60">Loading…</div>
        </div>

        <!-- Error -->
        <div
            v-else-if="game2.error.value"
            class="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400"
        >
            {{ game2.error.value }}
        </div>

        <template v-else>
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
                <!-- Left: upload / preview -->
                <section class="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-sm shadow-black/40">
                    <h2 class="text-lg font-semibold text-white">Upload an Image</h2>
                    <p class="mt-1 text-sm text-white/70">
                        Upload a meat image to get the AI prediction.
                    </p>

                    <label
                        class="mt-5 flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-white/15 bg-white/5 p-6 text-center transition hover:border-[#8c0a42]/60 hover:bg-[#8c0a42]/10"
                        :class="{ 'pointer-events-none opacity-70': hasPrediction }"
                    >
                        <input
                            ref="fileInputRef"
                            class="hidden"
                            type="file"
                            accept="image/*"
                            :disabled="hasPrediction"
                            @change="onFileChange"
                        />
                        <div class="flex items-center gap-3">
                            <div
                                class="grid h-10 w-10 place-items-center rounded-xl bg-[#8c0a42] shadow-lg shadow-[#8c0a42]/30"
                            >
                                <span class="text-sm font-bold text-white">↑</span>
                            </div>
                            <div>
                                <div class="text-sm font-semibold text-white">
                                    {{
                                        game2.selectedFile.value
                                            ? game2.selectedFile.value.name
                                            : "Select an image"
                                    }}
                                </div>
                                <div class="text-xs text-white/60">
                                    {{ hasPrediction ? "Image uploaded" : "or drag it here" }}
                                </div>
                            </div>
                        </div>
                    </label>

                    <div
                        v-if="displayImageUrl"
                        class="mt-4 aspect-video w-full overflow-hidden rounded-2xl border border-white/10 bg-black/30"
                    >
                        <img :src="displayImageUrl" alt="Uploaded image" class="h-full w-full object-contain" />
                    </div>
                </section>

                <!-- Right: whole workflow in one card -->
                <section class="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-sm shadow-black/40">
                    <!-- STEP 1 -->
                    <div>
                        <h2 class="text-lg font-semibold text-white">Your Initial Classification</h2>
                        <p class="mt-1 text-sm text-white/70">
                            Select the marbling category before seeing the AI result.
                        </p>

                        <div class="mt-4 grid grid-cols-2 gap-2">
                            <label
                                v-for="cls in FOUR_CLASSES"
                                :key="cls"
                                class="flex items-center gap-2 rounded-xl border px-3 py-2 text-zinc-500 transition"
                                :class="getFirstAnswerClass(cls)"
                            >
                                <input
                                    type="radio"
                                    name="g2-first"
                                    class="h-4 w-4 accent-[#8c0a42]"
                                    :value="cls"
                                    :checked="game2.firstAnswer.value === cls"
                                    :disabled="hasPrediction"
                                    @change="game2.firstAnswer.value = cls as any"
                                />
                                <span class="text-sm">{{ cls }}</span>
                            </label>
                        </div>

                        <div class="mt-5">
                            <p class="text-sm font-medium text-white">How confident are you in your answer?</p>
                            <div class="mt-2 flex gap-2">
                                <button
                                    v-for="n in 5"
                                    :key="n"
                                    type="button"
                                    class="flex-1 rounded-lg border py-2 text-sm font-semibold transition"
                                    :class="getFirstConfidenceClass(n)"
                                    :disabled="hasPrediction"
                                    @click="game2.firstConfidence.value = n"
                                >
                                    {{ n }}
                                </button>
                            </div>
                            <div class="mt-1 flex justify-between text-xs text-white/40">
                                <span>Very low</span>
                                <span>Very high</span>
                            </div>
                        </div>

                        <div class="mt-6 flex justify-end">
                            <button
                                v-if="!hasPrediction"
                                class="rounded-xl bg-[#8c0a42] px-6 py-2 text-sm font-semibold text-zinc-100 transition hover:bg-[#a00d4e] disabled:opacity-40"
                                :disabled="!canSubmitStep1 || game2.predicting.value"
                                @click="handlePredict"
                            >
                                {{ game2.predicting.value ? "Predicting…" : "Get AI Prediction" }}
                            </button>
                        </div>
                    </div>

                    <!-- STEP 2 -->
                    <div v-if="hasPrediction" class="mt-8 border-t border-white/10 pt-6">
                        <h2 class="text-lg font-semibold text-white">AI Prediction</h2>

                        <div class="mt-4 grid gap-3 sm:grid-cols-2">
                            <div class="rounded-xl border border-white/10 bg-black/20 p-3">
                                <div class="text-xs text-white/50">AI Predicted Class</div>
                                <div class="mt-1 text-sm font-semibold text-[#e0608a]">
                                    {{ game2.aiResult.value?.ai_prediction }}
                                </div>
                            </div>

                            <div class="rounded-xl border border-white/10 bg-black/20 p-3">
                                <div class="text-xs text-white/50">AI Confidence</div>
                                <div class="mt-1 text-sm font-semibold text-white">
                                    {{ aiConfidencePercent }}%
                                </div>
                                <div class="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                                    <div
                                        class="h-full rounded-full bg-[#8c0a42] transition-all"
                                        :style="{ width: aiConfidencePercent + '%' }"
                                    />
                                </div>
                            </div>
                        </div>

                        <div class="mt-6 flex justify-end">
                            <button
                                v-if="!showFinalSection"
                                class="rounded-xl bg-[#8c0a42] px-6 py-2 text-sm font-semibold text-white transition hover:bg-[#a00d4e]"
                                @click="game2.advanceToFinalStep()"
                            >
                                Continue to Final Answer
                            </button>
                        </div>
                    </div>

                    <!-- STEP 3 -->
                    <div v-if="showFinalSection" class="mt-8 border-t border-white/10 pt-6">
                        <h2 class="text-lg font-semibold text-white">Final Answer</h2>
                        <p class="mt-1 text-sm text-white/70">
                            After seeing the AI result, what is your final classification?
                        </p>

                        <div class="mt-4 grid grid-cols-2 gap-2">
                            <label
                                v-for="cls in FOUR_CLASSES"
                                :key="cls"
                                class="flex items-center gap-2 rounded-xl border px-3 py-2 text-zinc-500 transition"
                                :class="{
                                    'border-[#8c0a42] bg-[#8c0a42]/10 text-white':
                                        game2.finalAnswer.value === cls,
                                    'border-white/10 bg-black/20 hover:border-[#8c0a42]/50 hover:bg-[#8c0a42]/10':
                                        game2.finalAnswer.value !== cls,
                                }"
                            >
                                <input
                                    type="radio"
                                    name="g2-final"
                                    class="h-4 w-4 accent-[#8c0a42]"
                                    :value="cls"
                                    :checked="game2.finalAnswer.value === cls"
                                    @change="game2.finalAnswer.value = cls as any"
                                />
                                <span class="text-sm">{{ cls }}</span>
                            </label>
                        </div>

                        <div class="mt-5">
                            <p class="text-sm font-medium text-white/70">How much do you trust the AI prediction?</p>
                            <div class="mt-2 flex gap-2">
                                <button
                                    v-for="n in 5"
                                    :key="n"
                                    type="button"
                                    class="flex-1 rounded-lg border py-2 text-sm font-semibold transition"
                                    :class="
                                        game2.trustInAi.value === n
                                            ? 'border-[#8c0a42] bg-[#8c0a42] text-white'
                                            : 'border-white/10 bg-black/20 text-zinc-500 hover:border-[#8c0a42]/50'
                                    "
                                    @click="game2.trustInAi.value = n"
                                >
                                    {{ n }}
                                </button>
                            </div>
                            <div class="mt-1 flex justify-between text-xs text-white/40">
                                <span>Not at all</span>
                                <span>Completely</span>
                            </div>
                        </div>

                        <div class="mt-5">
                            <p class="text-sm font-medium text-white/70">
                                How confident do you think the AI is in its prediction?
                            </p>
                            <div class="mt-2 flex gap-2">
                                <button
                                    v-for="n in 5"
                                    :key="n"
                                    type="button"
                                    class="flex-1 rounded-lg border py-2 text-sm font-semibold transition"
                                    :class="
                                        game2.aiConfidenceRating.value === n
                                            ? 'border-[#8c0a42] bg-[#8c0a42] text-white'
                                            : 'border-white/10 bg-black/20 text-zinc-500 hover:border-[#8c0a42]/50'
                                    "
                                    @click="game2.aiConfidenceRating.value = n"
                                >
                                    {{ n }}
                                </button>
                            </div>
                            <div class="mt-1 flex justify-between text-xs text-white/40">
                                <span>Very uncertain</span>
                                <span>Very confident</span>
                            </div>
                        </div>

                        <div class="mt-6 flex justify-end">
                            <button
                                class="rounded-xl bg-[#8c0a42] px-6 py-2 text-sm font-semibold text-white transition hover:bg-[#a00d4e] disabled:opacity-40"
                                :disabled="!canSubmitFinal || game2.finalizing.value"
                                @click="handleFinalize"
                            >
                                {{ game2.finalizing.value ? "Submitting…" : "Submit Final Answer" }}
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useGame2 } from "../../composables/useGame2";
import { FOUR_CLASSES, type SubmitResult } from "../../types/game";

const props = defineProps<{
    sessionId: string;
    round: number;
}>();

const emit = defineEmits<{
    (e: "round-complete", result: SubmitResult): void;
}>();

const game2 = useGame2();
const fileInputRef = ref<HTMLInputElement | null>(null);

onMounted(() => {
    game2.loadRoundData(props.sessionId, props.round);
});

const canSubmitStep1 = computed(
    () =>
        !!game2.selectedFile.value &&
        !!game2.firstAnswer.value &&
        game2.firstConfidence.value != null,
);

const canSubmitFinal = computed(
    () =>
        !!game2.finalAnswer.value &&
        game2.trustInAi.value != null &&
        game2.aiConfidenceRating.value != null,
);

const aiConfidencePercent = computed(() => {
    const c = game2.aiResult.value?.ai_confidence ?? 0;
    return (Math.min(1, Math.max(0, c)) * 100).toFixed(1);
});

const hasPrediction = computed(() => !!game2.aiResult.value);
const showFinalSection = computed(
    () => game2.step.value === "final" || game2.step.value === "done",
);

const displayImageUrl = computed(() => {
    return game2.aiResult.value?.image_url || game2.previewUrl.value || null;
});

function onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    game2.onFileSelected(file);
    if (fileInputRef.value) fileInputRef.value.value = "";
}

async function handlePredict() {
    await game2.predictAndAdvance(props.sessionId, props.round);
}

async function handleFinalize() {
    const result = await game2.finalize();
    if (result) emit("round-complete", result);
}

function getFirstAnswerClass(cls: string) {
    if (hasPrediction.value) {
        const predicted = game2.aiResult.value?.ai_prediction;
        const first = game2.firstAnswer.value;

        if (predicted === cls) {
            return "border-green-500 bg-green-500/10 text-white";
        }

        if (first === cls && first !== predicted) {
            return "border-red-500 bg-red-500/10 text-white";
        }

        return "border-white/10 bg-black/20 text-zinc-500";
    }

    return game2.firstAnswer.value === cls
        ? "border-[#8c0a42] bg-[#8c0a42]/10 text-white"
        : "border-white/10 bg-black/20 hover:border-[#8c0a42]/50 hover:bg-[#8c0a42]/10";
}

function getFirstConfidenceClass(n: number) {
    const selected = game2.firstConfidence.value === n;

    if (hasPrediction.value) {
        return selected
            ? "border-[#8c0a42] bg-[#8c0a42] text-white"
            : "border-white/10 bg-black/20 text-zinc-500";
    }

    return selected
        ? "border-[#8c0a42] bg-[#8c0a42] text-white"
        : "border-white/10 bg-black/20 text-zinc-500 hover:border-[#8c0a42]/50";
}
</script>
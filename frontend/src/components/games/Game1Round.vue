<template>
    <div class="space-y-4">
        <!-- Loading -->
        <div v-if="game1.loading.value" class="flex items-center justify-center py-16">
            <div class="text-sm text-white/60">Loading image…</div>
        </div>

        <!-- Error -->
        <div
            v-else-if="game1.error.value"
            class="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400"
        >
            {{ game1.error.value }}
        </div>

        <template v-else-if="game1.roundData.value">
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
                <!-- Image -->
                <section class="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-sm shadow-black/40">
                    <h2 class="text-lg font-semibold text-white">Classify this image</h2>
                    <p class="mt-1 text-sm text-white/70">
                        Select the marbling class that best matches.
                    </p>

                    <div
                        class="mt-4 aspect-video w-full overflow-hidden rounded-2xl border border-white/10 bg-black/30"
                    >
                        <img
                            v-if="game1.roundData.value.image.image_url"
                            :src="game1.roundData.value.image.image_url"
                            alt="Classify this meat image"
                            class="h-full w-full object-contain"
                        />
                        <div v-else class="grid h-full place-items-center">
                            <div class="text-center">
                                <div class="text-4xl opacity-30">🥩</div>
                                <div class="mt-2 text-sm text-white/50">Placeholder image</div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Right panel -->
                <section class="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-sm shadow-black/40">
                    <h2 class="text-lg font-semibold text-white">Select a class</h2>

                    <div class="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                        <label
                            v-for="opt in NINE_CLASSES"
                            :key="opt"
                            class="flex items-center gap-2 rounded-xl border px-3 py-2 text-zinc-400 transition"
                            :class="getOptionClass(opt)"
                        >
                            <input
                                class="h-4 w-4 accent-[#8c0a42]"
                                type="radio"
                                name="game1-class"
                                :value="opt"
                                :checked="game1.selectedClass.value === opt"
                                :disabled="!!game1.result.value"
                                @change="game1.selectedClass.value = opt"
                            />
                            <span class="text-sm">{{ opt }}</span>
                        </label>
                    </div>

                    <!-- Confidence scale -->
                    <div class="mt-6 rounded-2xl border border-white/10 bg-black/20 p-4">
                        <p class="text-sm font-medium text-white">
                            How confident are you in your answer?
                        </p>

                        <div class="mt-3 flex gap-2">
                            <button
                                v-for="n in 5"
                                :key="n"
                                type="button"
                                class="flex-1 rounded-lg border py-2 text-sm font-semibold transition"
                                :class="getConfidenceClass(n)"
                                :disabled="!!game1.result.value"
                                @click="game1.confidence.value = n"
                            >
                                {{ n }}
                            </button>
                        </div>

                        <div class="mt-1 flex justify-between text-xs text-white/40">
                            <span>Very low</span>
                            <span>Very high</span>
                        </div>
                    </div>

                    <!-- Result shown in same view -->
                    <div v-if="game1.result.value" class="mt-6">
                        <h3 class="text-lg font-semibold text-white">Result</h3>

                        <div class="mt-4 flex items-center gap-3">
                            <div
                                class="rounded-full border px-4 py-1 text-sm font-bold"
                                :class="
                                    game1.result.value.answer.is_correct
                                        ? 'border-green-500/30 bg-green-500/20 text-green-400'
                                        : 'border-red-500/30 bg-red-500/20 text-red-400'
                                "
                            >
                                {{ game1.result.value.answer.is_correct ? "Correct!" : "Incorrect!" }}
                            </div>
                        </div>

                        <p class="mt-3 text-sm text-white/70">
                            <template v-if="game1.result.value.answer.is_correct">
                                You selected the correct class.
                            </template>
                            <template v-else>
                                Your selection is highlighted in red and the correct class is highlighted in green.
                            </template>
                        </p>

                        <div class="mt-3 grid gap-3 sm:grid-cols-2">
                            <div class="rounded-xl border border-white/10 bg-black/20 p-3">
                                <div class="text-xs text-white/50">Your answer</div>
                                <div class="mt-1 text-sm font-semibold text-white">
                                    {{ game1.result.value.answer.user_answer }}
                                </div>
                            </div>

                            <div class="rounded-xl border border-white/10 bg-black/20 p-3">
                                <div class="text-xs text-white/50">Correct answer</div>
                                <div class="mt-1 text-sm font-semibold text-[#e0608a]">
                                    {{ game1.result.value.answer.correct_answer }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-6 flex justify-end">
                        <button
                            v-if="!game1.result.value"
                            class="rounded-xl bg-[#8c0a42] px-6 py-2 text-sm font-semibold text-white transition hover:bg-[#a00d4e] disabled:opacity-40"
                            :disabled="
                                !game1.selectedClass.value ||
                                game1.confidence.value == null ||
                                game1.submitting.value
                            "
                            @click="handleSubmit"
                        >
                            {{ game1.submitting.value ? "Submitting…" : "Submit" }}
                        </button>

                        <button
                            v-else
                            class="rounded-xl bg-[#8c0a42] px-6 py-2 text-sm font-semibold text-zinc-100 transition hover:bg-[#a00d4e]"
                            @click="emit('round-complete', game1.result.value)"
                        >
                            Continue
                        </button>
                    </div>
                </section>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useGame1 } from "../../composables/useGame1";
import { NINE_CLASSES, type SubmitResult } from "../../types/game";

const props = defineProps<{
    sessionId: string;
    round: number;
}>();

const emit = defineEmits<{
    (e: "round-complete", result: SubmitResult): void;
}>();

const game1 = useGame1();

onMounted(() => {
    game1.loadRoundData(props.sessionId, props.round);
});

async function handleSubmit() {
    await game1.submit(props.sessionId, props.round);
}

function getSelectedAnswer(): string | null {
    if (game1.result.value?.answer?.user_answer) {
        return game1.result.value.answer.user_answer;
    }
    return game1.selectedClass.value;
}

function getCorrectAnswer(): string | null {
    return game1.result.value?.answer?.correct_answer ?? null;
}

function getOptionState(opt: string): "default" | "correct" | "wrong" | "selected" {
    if (!game1.result.value) {
        return game1.selectedClass.value === opt ? "selected" : "default";
    }

    const selected = getSelectedAnswer();
    const correct = getCorrectAnswer();

    if (correct && opt === correct) return "correct";
    if (selected && opt === selected && selected !== correct) return "wrong";

    return "default";
}

function getOptionClass(opt: string): string {
    const state = getOptionState(opt);

    if (state === "correct") {
        return "border-green-500 bg-green-500/10 text-white";
    }

    if (state === "wrong") {
        return "border-red-500 bg-red-500/10 text-white";
    }

    if (state === "selected") {
        return "cursor-pointer border-[#8c0a42] bg-[#8c0a42]/10 text-white";
    }

    return game1.result.value
        ? "border-white/10 bg-black/20 text-zinc-500"
        : "cursor-pointer border-white/10 bg-black/20 text-zinc-400 hover:border-[#8c0a42]/50 hover:bg-[#8c0a42]/10 hover:text-white";
}

function getConfidenceClass(n: number): string {
    const isSelected = game1.confidence.value === n;

    if (game1.result.value) {
        return isSelected
            ? "border-[#8c0a42] bg-[#8c0a42] text-white"
            : "border-white/10 bg-black/20 text-zinc-500";
    }

    return isSelected
        ? "border-[#8c0a42] bg-[#8c0a42] text-white"
        : "border-white/10 bg-black/20 text-zinc-500 hover:border-[#8c0a42]/50";
}
</script>
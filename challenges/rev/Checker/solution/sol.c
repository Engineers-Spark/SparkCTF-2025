#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MINI 32
#define MAXI 126
char rev_func(char c, int key) {
    int charac = c ^ key;
    while (charac < MINI) {
        charac += (MAXI - MINI + 1);
    }
    while (charac > MAXI) {
        charac -= (MAXI - MINI + 1);
    }
    return (char)charac;
}
int generate() {
    srand(455);
    return rand() % 100;
}

void reverse_rcifour(unsigned char *key, unsigned char *data, unsigned char *output, int len) {
    int i, j = 0, t;
    unsigned char S[256], K[256], temp;
    
    for (i = 0; i < 256; i++) {
        S[i] = i;
        K[i] = key[i % strlen((char *)key)];
    }
    
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + K[i]) % 256;
        temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }
    
    i = j = 0;
    for (t = 0; t < len; t++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        temp = S[i];
        S[i] = S[j];
        S[j] = temp;
        output[t] = data[t] ^ S[(S[i] + S[j]) % 256];
    }
}

void shuffle(char *str, unsigned int seed) {
    srand(seed);
    for (int i = 4; i >= 0; i--) {
        int shift = rand() % 6;
        int len = strlen(str);
        char temp[len + 1];
        for (int j = 0; j < len; j++) {
            temp[(j + shift) % len] = str[j];
        }
        temp[len] = '\0';
        strcpy(str, temp);
    }
}

int main() {
    char part1[] = "iJ[HQyn|Asem[TNenuNu";
    unsigned char part2[] = {0x11, 0xB4, 0xFE, 0xCF, 0x11, 0x9F, 0x68, 0x93, 0xED, 0x6E, 0x6B, 0xF4, 0x42, 0x78, 0xD2, 0xA2, 0x61, 0x69, 0x38, 0xF5, 0x82, 0x7D, 0x66};
    char shuff[] = "3147852";
    
    int key = generate();
    char dec_part1[21];
    for (int i = 0; i < 20; i++) {
        dec_part1[i] = rev_func(part1[i], key);
    }
    dec_part1[20] = '\0';
    
    unsigned char dec_part2[23];
    reverse_rcifour((unsigned char *)"Sparkieieie", part2, dec_part2, 23);
    dec_part2[23] = '\0';
    
    shuffle(shuff, 66);
    
    printf("Recovered password: %s%s%s}\n", dec_part1, dec_part2, shuff);
    return 0;
}

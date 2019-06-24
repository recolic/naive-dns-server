#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <openssl/pem.h>


static const unsigned char base64_table[65]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static unsigned char*base64_decode(const unsigned char*src,size_t len,size_t*out_len){unsigned char dtable[256],*out,*pos,block[4],tmp;
size_t i,count,olen;int pad=0;if(len==0){out_len=0;out=malloc(1);out[0]='\0';return out;}memset(dtable,0x80,256);for(i=0;i<sizeof
(base64_table)-1;i++)dtable[base64_table[i]]=(unsigned char)i;dtable['=']=0;count=0;for(i=0;i<len;i++){if(dtable[src[i]]!=0x80)
count++;}if(count==0||count%4)return NULL;olen=count/4*3;pos=out=malloc(olen);if(out==NULL)return NULL;count=0;for(i=0;i<len;i++)
{tmp=dtable[src[i]];if(tmp==0x80)continue;if(src[i]=='=')pad++;block[count]=tmp;count++;if(count==4){*pos++=(block[0]<<2)|(block[
1]>>4);*pos++=(block[1]<<4)|(block[2]>>2);*pos++=(block[2]<<6)|block[3];count=0;if(pad){if(pad==1)pos--;else if(pad==2)pos-=2
;else{free(out);return NULL;}break;}}}*out_len=pos-out;return out;}

static RSA * createRSA(const char *pem, int isPublic)
{
    RSA *rsa = NULL;
    FILE *pFile = fmemopen((void*)pem, strlen(pem), "r");
    if(isPublic)
        rsa = PEM_read_RSA_PUBKEY(pFile, &rsa,NULL, NULL);
    else
        rsa = PEM_read_RSAPrivateKey(pFile, &rsa,NULL, NULL);
    return rsa;
}
// return 1 for error, 0 for success
int do_decrypt(const char *hardcoded_key, const char *data, size_t data_len, void **output_data, size_t *output_data_len) {
    /* do_decrypt should free key_data & config_data if needed. */
    /* method is always rsa */
    RSA *pubKey = createRSA(hardcoded_key, 1);
    if(pubKey == NULL)
        return 1;

    *output_data = malloc(data_len);
    if(*output_data == NULL)
        return 1;
    
    printf("DEBUG: data=%s, dataLen=%ld\n", data, data_len);
//    size_t decoded_len = 0;
//    unsigned char *decoded_data = base64_decode(data, data_len, &decoded_len);
//
//    data_len = decoded_len;
//    printf("DEBUG: data=%s, dataLen=%ld\n", data, data_len);



    int cipherBlockSize = RSA_size(pubKey);
    /* int plainBlockSize = RSA_size(pubKey) - 11; */
    int plainIndex = 0;
    for(int index = 0; index < data_len; index += cipherBlockSize) {
        int flen = index + cipherBlockSize > data_len ? data_len - index : cipherBlockSize;
        printf("DEBUG> index=%d, flen=%d, \n", index, flen);
        int res = RSA_public_decrypt(flen, (unsigned char *)data + index, (unsigned char *)*output_data + plainIndex, pubKey, RSA_PKCS1_PADDING);
        if(res == -1) {
            printf("RSA_public_decrypt failed. ERR_get_error() = %ld. \n", ERR_get_error());
            //free(*output_data);
            //*output_data = NULL;
            return 1;
        }
        plainIndex += res;
    }
    *output_data_len = plainIndex;

//do_dec_err:
    // Called from Python: Do not free data.
    // free(data);
    return 0;
}
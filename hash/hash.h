#ifndef _HASH_H_
#define _HASH_H_

#include <string>

#include "ed2k.h"

#include <openssl/md4.h>
#include <openssl/md5.h>
#include <openssl/sha.h>

class Hash {
	private:
		bool finished;
		
		int crc32_ctx;
		std::string crc32_str;
		
		Ed2k ed2k_ctx;
		std::string ed2k_str;
		
		MD5_CTX md5_ctx;
		std::string md5_str;
		
		SHA_CTX sha1_ctx;
		std::string sha1_str;
		
	public:
		Hash();
		void update(std::string data);
		std::string crc32();
		std::string ed2k();
		std::string md5();
		std::string sha1();
};

#endif // _HASH_H_

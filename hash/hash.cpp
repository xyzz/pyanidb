#include "hash.h"
#include "crc32.h"

#include <stdexcept>

namespace Hex {
	static char* digits = "0123456789abcdef";
	std::string hex(char* bin, int length) {
		std::string s(length * 2, ' ');
		for(int i = 0; i < length; i++) {
			s[i*2] = digits[(bin[i] >> 4) & 0xf];
			s[i*2+1] = digits[bin[i] & 0xf];
		}
		return s;
	}
	std::string hex(int bin) {
		std::string s(sizeof(int) * 2, ' ');
		for(int i = 0; i < sizeof(int) * 2; i++) {
			s[sizeof(int) * 2 - 1 - i] = digits[bin & 0xf];
			bin = bin >> 4;
		}
		return s;
	}
}

Hash::Hash() {
	finished = false;
	
	crc32_ctx = 0;
	crc32_str = "";
	
	ed2k_str = "";
	
	MD5_Init(&md5_ctx);
	md5_str = "";
	
	SHA1_Init(&sha1_ctx);
	sha1_str = "";
}

void Hash::update(std::string data) {
	if(finished) {
		throw std::runtime_error("Can't update after digest.");
	}
	crc32_ctx = CRC32::crc32(crc32_ctx, data.c_str(), data.length());
	ed2k_ctx.update(data.c_str(), data.length());
	MD5_Update(&md5_ctx, data.c_str(), data.length());
	SHA1_Update(&sha1_ctx, data.c_str(), data.length());
}

std::string Hash::crc32() {
	return Hex::hex(crc32_ctx);
}

std::string Hash::ed2k() {
	if(!ed2k_str.length()) {
		finished = true;
		char* digest = ed2k_ctx.digest();
		ed2k_str = Hex::hex(digest, 16);
		delete digest;
	}
	return ed2k_str;
}

std::string Hash::md5() {
	if(!md5_str.length()) {
		finished = true;
		char* digest = new char[16];
		MD5_Final((unsigned char*)digest, &md5_ctx);
		md5_str = Hex::hex(digest, 16);
		delete digest;
	}
	return md5_str;
}

std::string Hash::sha1() {
	if(!sha1_str.length()) {
		finished = true;
		char* digest = new char[20];
		SHA1_Final((unsigned char*)digest, &sha1_ctx);
		sha1_str = Hex::hex(digest, 20);
		delete digest;
	}
	return sha1_str;
}

#include <iostream>
#include <sstream>
#include <iomanip>

std::string hexToString(const std::string& hex) {
    std::string result;
    for (size_t i = 0; i < hex.length(); i += 2) {
        std::string byte = hex.substr(i, 2);
        char chr = (char)strtol(byte.c_str(), nullptr, 16);
        result.push_back(chr);
    }
    return result;
}

int main() {
    std::string hexString = "4449443A494D53493A376131363634373037373665306338626365643039613065303064613739326366326631376630316231646366386333386264643863353835383261326634653534636262306661653265323561333633383836653239353332663039363237303431336236373262343734623238313332353637333233633866316134333930";
    
    std::string decodedString = hexToString(hexString);
    
    // 输出解码后的结果
    std::cout << "Decoded string: " << decodedString << std::endl;
    
    return 0;
}


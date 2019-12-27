const zip = require('./utils').zip;

class TrieNode {
    constructor(isEndOfWord, length = 26) {
        this.childNodes = new Map(zip(Array.from('abcdefghijklmnopqrstuvwxyz'), new Array(length)));
        this.isEndOfWord = isEndOfWord;
    }

    insert(key) {
        let currentNode = this;
        let childNode;

        for(const letter of key) {
            childNode = currentNode.childNodes.get(letter) || new TrieNode(false);
            currentNode.childNodes.set(letter, childNode);
            currentNode = childNode;
        }

        currentNode.isEndOfWord = true;
    }

    search(key, fullWord = false) {
        let currentNode = this;

        for(const letter of key) {
            if(currentNode.childNodes.get(letter) === undefined)
                return false;
            
            currentNode = currentNode.childNodes.get(letter);
        }

        if(fullWord)
            return true && currentNode.isEndOfWord;
        
        return true;
    }

    static searchDownTheTree(trieNode, wordUpTheTree, matches) {
        trieNode && trieNode.childNodes.forEach((value, alphabet) => {
            if(value && value.isEndOfWord) {
                matches.push(wordUpTheTree + alphabet);
            }

            TrieNode.searchDownTheTree(value, wordUpTheTree + alphabet, matches);
        });
    }

    getAllMatches(key) {
        const matches = [];
        let currentNode = this;

        for(const letter of key) {
            if(currentNode.childNodes.get(letter) === undefined)
                return matches;
            
            currentNode = currentNode.childNodes.get(letter);
        }

        TrieNode.searchDownTheTree(currentNode, key, matches);
        return matches;
    }
}

const trieNode = new TrieNode(false);
trieNode.insert('latish');
trieNode.insert('laa');
trieNode.insert('lapavan');
trieNode.insert('latishpavan');
console.log(trieNode.getAllMatches('la'));

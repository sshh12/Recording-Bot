'use strict';

const fs = require('fs');
const path = require('path');
const Discord = require('discord.js');
const opus = require('node-opus');

const datapath = 'voicedata';
const rate = 48000;
const frame_size = 1920;
const channels = 2;
const pythonapp = 'bot_conversation.py'
const token = '';

const child = require('child_process');

let voiceConnections = new Map();
let voiceReceivers = new Map();
let writeStreams = new Map();

let client = new Discord.Client()

let textChannel;

client.on('ready', () => {
    console.log("Started!");
});

client.on('message', (msg) => {
    if (msg.content.charAt(0) === '!') {
        switch (msg.content.slice(1)) {
            case 'on':
				textChannel = msg.channel;
                start(msg.member);
                break;
            case 'off':
                stop(msg.member);
                break;
        }
    }
});

client.on('guildMemberSpeaking', (member, speaking) => {

    if (!speaking && member.voiceChannel) {
        let receiver = voiceReceivers.get(member.voiceChannelID);
        if (receiver) {
            let writeStream = writeStreams.get(member.id);
            if (writeStream) {
                writeStreams.delete(member.id);
                writeStream.end((err) => {
                    if (err) {
                        console.error(err);
                    } else {
                        let pcmpath = writeStream.path.replace(".opus_hex", ".pcm_raw");
                        save(writeStream.path, pcmpath, member);
                    }
                });
            }
        }
    }

});

let start = (member) => {

    if (!member || !member.voiceChannel) {
        return;
    }

    member.voiceChannel.join().then((voiceConnection) => {

        console.log("Recording...");

        voiceConnections.set(member.voiceChannelID, voiceConnection);
        let voiceReceiver = voiceConnection.createReceiver();
        voiceReceiver.on('opus', (user, data) => {
            let hexString = data.toString('hex');
            let writeStream = writeStreams.get(user.id);
            if (!writeStream) {
                if (hexString === 'f8fffe') {
                    return;
                }
                let outputPath = path.join(datapath, `${Date.now()}.opus_hex`);
                writeStream = fs.createWriteStream(outputPath);
                writeStreams.set(user.id, writeStream);
            }
            writeStream.write(`,${hexString}`);
        });
        voiceReceivers.set(member.voiceChannelID, voiceReceiver);
    }).catch(console.error);

}

let stop = (member) => {

    if (!member || !member.voiceChannel) {
        return;
    }

    console.log("Stopping...");

    if (voiceReceivers.get(member.voiceChannelID)) {
        voiceReceivers.get(member.voiceChannelID).destroy();
        voiceReceivers.delete(member.voiceChannelID);
        voiceConnections.get(member.voiceChannelID).disconnect();
        voiceConnections.delete(member.voiceChannelID);
    }

}

let save = (inputPath, filename, member) => {

    let encoder = new opus.OpusEncoder(rate, channels);
    const inputStream = fs.createReadStream(inputPath);
    const outputStream = fs.createWriteStream(filename);
    let data = '';

    inputStream.on('data', chunk => {
        data += chunk.toString();
        const frames = data.split(',');
        if (frames.length) {
            data = frames.pop();
        }
        for (let frame of frames) {
            if (frame !== '') {
                const decodedBuffer = getDecodedFrame(frame, encoder, filename);
                if (decodedBuffer) {
                    outputStream.write(decodedBuffer);
                }
            }
        }
    });

    inputStream.on('end', () => {
        outputStream.end((err) => {
            if (err) {
                console.error(err);
            } else {
                let py = child.spawn('python3', [pythonapp, 'open',  filename, ""+member.id, ""+Date.now()]);
                py.stdout.on('data', function(data) {
                    let content = data.toString().trim();
                    console.log(content);
                    if (content.startsWith("msg")) {
                        console.log(">> sending message");
                        textChannel.send(content.slice(4));
                    } else if (content.startsWith("play")) {
                        console.log(">> playing audio");
                        playFile(member, "./" + datapath + "/" + content.slice(5));
                    }
                });
            }
        });
    });

};

let getDecodedFrame = (frameString, encoder, filename) => {
    let buffer = Buffer.from(frameString, 'hex');
    try {
        buffer = encoder.decode(buffer, frame_size);
    } catch (err) {
        try {
            buffer = encoder.decode(buffer.slice(8), frame_size);
        } catch (err) {
            console.log(`${filename} was unable to be decoded`);
            return null;
        }
    }
    return buffer;
};

let playFile = (member, filename) => {
  let voiceConnection = voiceConnections.get(member.voiceChannelID)
  let disp = voiceConnection.playFile(filename);
  disp.on("end", (end) => {});
}

client.login(token).catch(console.error);

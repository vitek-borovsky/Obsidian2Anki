## Obsidian to anki

Goal:
- A way to read obsidian vault and create anki cards from them
- Vault file looks stil good and doesn't look *robotic*
- Does **NOT** make changes to my vault (main reason for this)
- If it renders as valid obsidian callout (with anki key) it get's added


Why not just use [Obsidian_to_Anki](https://github.com/ObsidianToAnki/Obsidian_to_Anki) ?
It creates syntax in vaults that I don't like the *robotic* look of
```
STARTI [{Note Type}] {Note Data} ENDI
STARTI [Basic] This is a test. Back: Test successful! ENDI

START
{Note Type}
{Note Fields}
Tags:
END

// Awful generated Id like
START
Basic
This is a test.
Back: Test successful!
<!--ID: 1566052191670-->
END

TARGET DECK
Mathematics

TARGET DECK: Mathematics
```
but if you are looking for feature-rich solution, this project is not for you and refer to [Obsidian_to_Anki](https://github.com/ObsidianToAnki/Obsidian_to_Anki)

### Terminology
file = obsidian's '.md' file
note/card = Anki's object

### Getting started
In your file's metadata define `Anki` Property (as for now must be exact match).
This property will determine the name of a **DECK**, use slashes for nesting (optionally you can use anki's build in '::' nesting)
> [!metadata]-
> Metadata are defined between '---' in obsidian
> > [!tip] Look if it get's formated normaly and you don't see any weird artifacts in *reading mode*
> Default behaviour of obsidian is you don't see anything

Then you can create card's with `> [!anki]` and `> [!ankiR]` Callouts (currently only these two are supported)

### Example usage
```md
---
Anki: Test_deck/subdeck
---

// Makes 'basic' card
> [!anki]- What is the answer to the ultimate question of life, universe, and everything?
> 42

// Makes 'basic and reversed' card
> [!ankiR]- What came before chicken?
> What came before egg?


This will create 3 cards and 2 notes as per anki terminology (i.e. one normal and one two-sided card)
```

### Running the script
```bash
https://github.com/vitek-borovsky/Obsidian2Anki.git

python src/main.py <path-to-your-vault>
```

### Support of nested callouts
```md
> [!note] This is outer callout
> > [!anki]- This is inner callout
> > text
```
> [!warn]- Nested callouts does not work on anki style callouts
> you can't have
> ```md
> > [!anki] out
> > > [!anki] in
> > > body
> ```
> only the outer one will be registred

### My callout css
Put this in `<Vault>/.obsidian/snippets/anki-callouts.css`
Enable in settings -> Apperance -> Css snippets -> anki-callouts

Restarting obsidian might be neccessary
```css
.callout[data-callout="anki"],
.callout[data-callout="ankir"],
.callout[data-callout="ankiR"] {
    --callout-color: 26, 64, 235;
    /* anki svg  */
    --callout-icon: '<svg x="0px" y="0px" width="100" height="100" viewBox="0 0 50 50"> <path d="M 12.84375 2 C 9.65575 2 7 4.852 7 8 L 7 42 C 7 43.863 7.92175 45.39125 9.09375 46.40625 C 10.26575 47.42125 11.68 48 13 48 L 37.375 48 C 40.465 48 43 45.465 43 42.375 L 43 7.625 C 43 4.535 40.465 2 37.375 2 L 12.84375 2 z M 12.84375 4 L 37.375 4 C 39.383 4 41 5.617 41 7.625 L 41 28.027344 C 32.292 21.256344 21.3 16.865188 9 15.242188 L 9 8 C 9 6.051 10.93775 4 12.84375 4 z M 35.03125 6.7109375 C 34.848625 6.7235625 34.668672 6.7869375 34.513672 6.8984375 L 31.980469 8.7285156 L 29.035156 7.6796875 C 28.677156 7.5506875 28.276906 7.6372969 28.003906 7.9042969 C 27.730906 8.1692969 27.631047 8.5657344 27.748047 8.9277344 L 28.705078 11.904297 L 26.798828 14.380859 C 26.566828 14.682859 26.525359 15.089641 26.693359 15.431641 C 26.861359 15.772641 27.208844 15.989234 27.589844 15.990234 L 30.714844 15.998047 L 32.480469 18.578125 C 32.668469 18.853125 32.979641 19.013672 33.306641 19.013672 C 33.353641 19.013672 33.400266 19.010906 33.447266 19.003906 C 33.824266 18.949906 34.136859 18.686219 34.255859 18.324219 L 35.230469 15.353516 L 38.228516 14.470703 C 38.593516 14.363703 38.866641 14.058594 38.931641 13.683594 C 38.996641 13.308594 38.843156 12.929078 38.535156 12.705078 L 36.011719 10.861328 L 36.099609 7.7363281 C 36.110609 7.3553281 35.905359 7.0022187 35.568359 6.8242188 C 35.399859 6.7352187 35.213875 6.6983125 35.03125 6.7109375 z M 34.042969 9.7050781 L 33.996094 11.330078 C 33.987094 11.659078 34.14025 11.973969 34.40625 12.167969 L 35.71875 13.125 L 34.160156 13.583984 C 33.844156 13.676984 33.595188 13.918469 33.492188 14.230469 L 32.986328 15.775391 L 32.068359 14.435547 C 31.882359 14.163547 31.573141 13.999047 31.244141 13.998047 L 29.619141 13.994141 L 30.611328 12.707031 C 30.812328 12.447031 30.873484 12.104016 30.771484 11.791016 L 30.273438 10.244141 L 31.804688 10.789062 C 32.114688 10.898062 32.458609 10.852203 32.724609 10.658203 L 34.042969 9.7050781 z M 9 17.259766 C 21.43 18.943766 32.45 23.536562 41 30.601562 L 41 42.375 C 41 44.387 39.387 46 37.375 46 L 13 46 C 12.32 46 11.23425 45.62125 10.40625 44.90625 C 9.57825 44.19125 9 43.215 9 42 L 9 17.259766 z M 20.953125 22.90625 C 20.388125 22.97425 19.919469 23.349719 19.730469 23.886719 L 17.964844 28.900391 L 12.830078 30.289062 C 12.281078 30.438063 11.872672 30.877547 11.763672 31.435547 C 11.653672 31.993547 11.866359 32.554391 12.318359 32.900391 L 16.542969 36.130859 L 16.275391 41.439453 C 16.246391 42.008453 16.539109 42.534547 17.037109 42.810547 C 17.264109 42.937547 17.511766 43 17.759766 43 C 18.054766 43 18.347563 42.910375 18.601562 42.734375 L 22.978516 39.716797 L 27.943359 41.609375 C 28.474359 41.814375 29.065422 41.7005 29.482422 41.3125 C 29.900422 40.9255 30.058484 40.345781 29.896484 39.800781 L 28.378906 34.703125 L 31.714844 30.566406 C 32.071844 30.123406 32.14625 29.526766 31.90625 29.009766 C 31.66525 28.495766 31.16275 28.164391 30.59375 28.150391 L 25.279297 28.021484 L 22.375 23.570312 C 22.064 23.091313 21.521125 22.84325 20.953125 22.90625 z M 21.269531 25.537109 L 23.751953 29.341797 C 24.019953 29.750797 24.470984 30.002625 24.958984 30.015625 L 29.501953 30.126953 L 26.650391 33.662109 C 26.342391 34.044109 26.242812 34.552578 26.382812 35.017578 L 27.679688 39.371094 L 23.435547 37.753906 C 22.978547 37.579906 22.465453 37.641969 22.064453 37.917969 L 18.324219 40.496094 L 18.552734 35.962891 C 18.578734 35.473891 18.359703 35.003031 17.970703 34.707031 L 14.361328 31.947266 L 18.744141 30.761719 C 19.216141 30.635719 19.597719 30.283312 19.761719 29.820312 L 21.269531 25.537109 z"></path> </svg>'
}
```

### Regex
It matches the regex of `(> )+\[!KEY\][+-]?.*`, where key is the note type (e.g. anki, AnkiR ...)
